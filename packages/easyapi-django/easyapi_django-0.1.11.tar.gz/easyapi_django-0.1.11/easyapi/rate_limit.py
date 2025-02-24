import os
import time
from redis import StrictRedis

REDIS_DB = os.environ['REDIS_DB']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PREFIX = os.environ.get('REDIS_PREFIX', '')


class RateLimit(StrictRedis):
    def __init__(self):
        super().__init__(host=REDIS_SERVER, db=REDIS_DB)

    def current_milli_time(self):
        return int(round(time.time() * 1000))

    def check_limits(self, identifier, limit_type=None):
        now = self.current_milli_time()
        type_to_check = limit_type if limit_type else "api"

        # Configurações fixas
        configs = {
            "api": {"interval": 1000, "limit": 5, "key": f"{REDIS_PREFIX}:limits:api:{identifier}"},
            "login": {"interval": 5000, "limit": 3, "key": f"{REDIS_PREFIX}:limits:login:{identifier}"},
            "abuse": {"interval": 5000, "limit": 30, "key": f"{REDIS_PREFIX}:limits:requests:{identifier}"}
        }

        config = configs.get(type_to_check, configs["api"])
        config_abuse = configs["abuse"]

        # Pipeline para operações do tipo específico e abuso
        p = self.pipeline()

        # Operações para o tipo específico
        p.zremrangebyscore(config["key"], 0, now - config["interval"])
        p.zcard(config["key"])  # Conta antes de adicionar
        p.zadd(config["key"], {f"req_{now}": now})
        p.expire(config["key"], int(config["interval"] / 1000) + 1)  # TTL em segundos

        # Operações para abuso
        p.zremrangebyscore(config_abuse["key"], 0, now - config_abuse["interval"])
        p.zcard(config_abuse["key"])  # Conta antes de adicionar
        p.zadd(config_abuse["key"], {f"req_{now}": now})
        p.expire(config_abuse["key"], int(config_abuse["interval"] / 1000) + 1)  # TTL em segundos

        pipeline_results = p.execute()

        # Resultados para o tipo específico
        count_type = pipeline_results[1]  # ZCARD antes de adicionar
        is_rate_limited = count_type >= config["limit"]

        # Resultados para abuso
        count_abuse = pipeline_results[5]  # ZCARD antes de adicionar
        is_abuse = count_abuse >= config_abuse["limit"]

        return {
            "rate_limited": is_rate_limited,
            "abuse": is_abuse
        }

    def api_limited(self, identifier):
        return self.check_limits(identifier, "api")

    def login_limited(self, identifier):
        return self.check_limits(identifier, "login")


RateLimiter = RateLimit()

import os
import time
from redis import StrictRedis

REDIS_DB = os.environ['REDIS_DB']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PREFIX = os.environ.get('REDIS_PREFIX', '')

class RateLimit(StrictRedis):
    def __init__(self, expire=None):
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
        p.zrange(config["key"], 0, -1, withscores=True)  # Pega todos os timestamps
        p.zadd(config["key"], {f"req_{now}": now})  # Usa string única como member

        # Operações para abuso
        p.zremrangebyscore(config_abuse["key"], 0, now - config_abuse["interval"])
        p.zcard(config_abuse["key"])  # Conta antes de adicionar
        p.zrange(config_abuse["key"], 0, -1, withscores=True)  # Pega todos os timestamps
        p.zadd(config_abuse["key"], {f"req_{now}": now})

        pipeline_results = p.execute()

        # Resultados para o tipo específico
        count_type = pipeline_results[1]  # ZCARD antes de adicionar
        all_timestamps_type = pipeline_results[2]  # Todos os timestamps
        is_rate_limited = count_type >= config["limit"]

        # Resultados para abuso
        count_abuse = pipeline_results[5]  # ZCARD antes de adicionar
        all_timestamps_abuse = pipeline_results[6]  # Todos os timestamps
        is_abuse = count_abuse >= config_abuse["limit"]

        # Calcula retry_after
        retry_after = 0

        if is_rate_limited and all_timestamps_type:
            # Calcula quantos precisam expirar para liberar o limite
            excess = count_type - config["limit"] + 1  # +1 para abrir espaço para a próxima
            if excess <= len(all_timestamps_type):
                # Pega o timestamp que, ao expirar, reduzirá o contador o suficiente
                expire_timestamp = int(float(all_timestamps_type[excess - 1][1]))
                retry_after_type = max(0, (expire_timestamp + config["interval"]) - now)
                retry_after = retry_after_type
            else:
                # Caso extremo: todos os timestamps precisam expirar
                retry_after = config["interval"]

        if is_abuse and all_timestamps_abuse:
            excess_abuse = count_abuse - config_abuse["limit"] + 1
            if excess_abuse <= len(all_timestamps_abuse):
                expire_timestamp_abuse = int(float(all_timestamps_abuse[excess_abuse - 1][1]))
                retry_after_abuse = max(0, (expire_timestamp_abuse + config_abuse["interval"]) - now)
                if is_rate_limited:
                    retry_after = min(retry_after, retry_after_abuse)
                else:
                    retry_after = retry_after_abuse
            else:
                retry_after = max(retry_after, config_abuse["interval"]) if is_rate_limited else config_abuse["interval"]

        return {
            "rate_limited": is_rate_limited,
            "abuse": is_abuse,
            "retry_after": retry_after
        }

    def api_limited(self, identifier):
        return self.check_limits(identifier, "api")

    def login_limited(self, identifier):
        return self.check_limits(identifier, "login")

RateLimiter = RateLimit()

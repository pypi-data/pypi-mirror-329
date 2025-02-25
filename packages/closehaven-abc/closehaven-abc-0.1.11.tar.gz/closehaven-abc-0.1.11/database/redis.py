import json
import random
import redis


async def redis_client(host, port):
	redis_client = redis.Redis(
		host=host,
		port=port,
		decode_responses=True  
	)
	return redis_client


async def set_cache(key: str, value: dict, redis_client_data:dict, expire_minutes: float, allow_random: bool = False):
  try:
    r_client = await redis_client(redis_client_data["host"],redis_client_data["port"])
    r_client.set(name=key, value=json.dumps(value), ex=(expire_minutes*random.randint(60, 120) if allow_random else expire_minutes*60))

  except Exception as e:
    raise e


async def get_cache(key: str, redis_client_data:dict):
  try:
    r_client = await redis_client(redis_client_data["host"],redis_client_data["port"])
    value = r_client.get(key)
    return json.loads(value) if value else None

  except Exception as e:
    raise e
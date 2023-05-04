#обработчик извлечение из кэша(внешняя функция в кот определен декоратор) на вход получает: (имя кэша и кэш конфиг),
#внешняя функция подключается к кэшу, задача декоратора-посмотреть есть ли чтото в кэше, если он извлечет, то он это и вернет
#иначе занесет в кэш и вернули
#создаем декоратор, который принимает декорируюмую функцию f, принимает любое неименованное параметров и  именованных параметорв
# (у нас именнованые), извлечение из кэша, если кшд_велью определено то и возвращаем, иначе запускаем декорируюмую функцию,
#это функцией будет селект и тогда респонз это значения извлеченные из БД, то потом заносим это в кэш, чтобы в след раз извлечь,
#возвращает имя декоратора, ttl - время жизни

from functools import wraps
from cache.connection import RedisCache

def fetch_from_cache(cache_name: str, cache_config: dict):

    cache_conn = RedisCache(cache_config['redis'])

    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name)
            if cached_value:
                return cached_value
            response = f(*args, **kwargs)
            print('response=', response)
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response
        return wrapper
    return wrapper_func

# noqa: F401
"""
    functions_cache.engines
    ~~~~~~~~~~~~~~~~~~~~~~~

    Classes and functions for cache persistence
"""


from .base import ENGINE_KWARGS, BaseCache

registry = {
    'memory': BaseCache,
}

_engine_dependencies = {
    'sqlite': 'sqlite3',
    'mongo': 'pymongo',
    'redis': 'redis',
    'dynamodb': 'dynamodb',
}

try:
    # Heroku doesn't allow the SQLite3 module to be installed
    from .sqlite import DbCache

    registry['sqlite'] = DbCache
except ImportError:
    DbCache = None

try:
    from .mongo import MongoCache

    registry['mongo'] = registry['mongodb'] = MongoCache
except ImportError:
    MongoCache = None


try:
    from .gridfs import GridFSCache

    registry['gridfs'] = GridFSCache
except ImportError:
    GridFSCache = None

try:
    from .redis import RedisCache

    registry['redis'] = RedisCache
except ImportError:
    RedisCache = None

try:
    from .dynamodb import DynamoDbCache

    registry['dynamodb'] = DynamoDbCache
except ImportError:
    DynamoDbCache = None


def create_engine(engine_name, cache_name, options):
    if isinstance(engine_name, BaseCache):
        return engine_name

    if engine_name is None:
        engine_name = _get_default_engine_name()
    try:
        return registry[engine_name](cache_name, **options)
    except KeyError:
        if engine_name in _engine_dependencies:
            raise ImportError('You must install the python package: %s' % _engine_dependencies[engine_name])
        else:
            raise ValueError('Unsupported engine "%s" try one of: %s' % (engine_name, ', '.join(registry.keys())))


def _get_default_engine_name():
    if 'sqlite' in registry:
        return 'sqlite'
    return 'memory'


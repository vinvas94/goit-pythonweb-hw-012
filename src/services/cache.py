from aiocache import caches

# Caching configuration settings for using Redis
caches.set_config(
    {
        "default": {
            "cache": "aiocache.RedisCache",  # Cache type - Redis
            "endpoint": "localhost",  # Redis server address
            "port": 6379,  # Redis server port
            "timeout": 10,  # Timeout for response
            "serializer": {
                "class": "aiocache.serializers.PickleSerializer"
            },  # Serializer for caching data
        }
    }
)

"""
Caching Layer for API Response Optimization
Implements Redis-based caching with fallback to in-memory cache
"""

import json
import hashlib
import time
from typing import Optional, Callable, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching for API responses"""
    
    def __init__(self, redis_client=None, ttl_seconds: int = 300):
        self.redis = redis_client
        self.ttl = ttl_seconds
        self.in_memory_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _generate_key(self, prefix: str, params: dict) -> str:
        """Generate cache key from prefix and parameters"""
        params_str = json.dumps(params, sort_keys=True, default=str)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f"{prefix}:{params_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            # Try Redis first
            if self.redis:
                value = self.redis.get(key)
                if value:
                    self.cache_hits += 1
                    return json.loads(value)
            
            # Fall back to in-memory cache
            if key in self.in_memory_cache:
                cached_value, expiry_time = self.in_memory_cache[key]
                if time.time() < expiry_time:
                    self.cache_hits += 1
                    return cached_value
                else:
                    del self.in_memory_cache[key]
            
            self.cache_misses += 1
            return None
        
        except Exception as e:
            logger.warning(f"Cache retrieval error: {e}")
            self.cache_misses += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        ttl = ttl or self.ttl
        
        try:
            # Try Redis first
            if self.redis:
                self.redis.setex(
                    key,
                    ttl,
                    json.dumps(value, default=str)
                )
                return True
            
            # Fall back to in-memory cache
            self.in_memory_cache[key] = (value, time.time() + ttl)
            return True
        
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.redis:
                self.redis.delete(key)
            if key in self.in_memory_cache:
                del self.in_memory_cache[key]
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        count = 0
        try:
            if self.redis:
                for key in self.redis.scan_iter(match=pattern):
                    self.redis.delete(key)
                    count += 1
            
            keys_to_delete = [k for k in self.in_memory_cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.in_memory_cache[key]
                count += 1
            
            return count
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "in_memory_size": len(self.in_memory_cache)
        }


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def init_cache(redis_client=None, ttl_seconds: int = 300) -> CacheManager:
    """Initialize global cache manager"""
    global _cache_manager
    _cache_manager = CacheManager(redis_client, ttl_seconds)
    return _cache_manager


def get_cache() -> CacheManager:
    """Get global cache manager instance"""
    if _cache_manager is None:
        init_cache()
    return _cache_manager


def cache_endpoint(prefix: str, ttl_seconds: int = 300):
    """
    Decorator for caching API endpoint responses.
    
    Usage:
        @cache_endpoint("battery_soh", ttl_seconds=600)
        async def predict_battery_health(request):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = get_cache()._generate_key(prefix, kwargs)
            
            # Check cache
            cached_result = get_cache().get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            get_cache().set(cache_key, result, ttl_seconds)
            
            return result
        
        return wrapper
    
    return decorator


def invalidate_cache(pattern: str):
    """Invalidate all cache keys matching pattern"""
    count = get_cache().clear_pattern(pattern)
    logger.info(f"Invalidated {count} cache entries matching pattern: {pattern}")

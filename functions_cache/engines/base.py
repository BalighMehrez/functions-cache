#!/usr/bin/env python
"""
    functions_cache.engines.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains BaseCache class which can be used as in-memory cache engine or
    extended to support persistence.
"""
import hashlib
from datetime import datetime, timezone
from io import BytesIO
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from functions_cache.function_identifier import FunctionIdentifier


# All engine-specific keyword arguments combined
ENGINE_KWARGS = [
    'connection',
    'db_name',
    'endpont_url',
    'extension',
    'fast_save',
    'ignored_parameters',
    'include_get_headers',
    'location',
    'name',
    'namespace',
    'read_capacity_units',
    'region_name',
    'write_capacity_units',
]



class BaseCache(object):
    """Base class for cache implementations, can be used as in-memory cache.

    To extend it you can provide dictionary-like objects for
    :attr:`responses` or override public methods.
    """

    def __init__(self, *args, **kwargs):
        #: `key_in_cache` -> `response` mapping
        self.responses = {}

    def save_response(self, key, response):
        """Save response to cache

        :param key: key for this response
        :param response: response to save

        """
        self.responses[key] = response, datetime.now(timezone.utc)

    def get_response_and_time(self, key, default=(None, None)):
        """Retrieves response and timestamp for `key` if it's stored in cache,
        otherwise returns `default`

        :param key: key of resource
        :param default: return this if `key` not found in cache
        :returns: tuple (response, datetime)

        """
        try:
            response, timestamp = self.responses[key]
        except KeyError:
            return default
        return response, timestamp

    def delete(self, key):
        """Delete `key` from cache. Also deletes all responses from response history"""
        try:
            if key in self.responses:
                response, _ = self.responses[key]
                del self.responses[key]
        except KeyError:
            pass

    def clear(self):
        """Clear cache"""
        self.responses.clear()

    def remove_old_entries(self, expires_before):
        """Deletes entries from cache with expiration time older than ``expires_before``"""
        if expires_before.tzinfo is None:
            # if expires_before is not timezone-aware, assume local time
            expires_before = expires_before.astimezone()

        keys_to_delete = set()
        for key, (response, _) in self.responses.items():
            if response.expiration_date is not None and response.expiration_date < expires_before:
                keys_to_delete.add(key)

        for key in keys_to_delete:
            self.delete(key)

    

    def create_key(self, function_identifier: FunctionIdentifier):
        key = hashlib.sha256()
        key.update(_to_bytes(function_identifier.function_name.upper()))
        
        if function_identifier.function_args and function_identifier.function_args != ():
            for arg in function_identifier.function_args:
                key.update(_to_bytes(arg))
            
        if function_identifier.function_kwargs and function_identifier.function_kwargs != ():
            for name, value in sorted(function_identifier.function_kwargs.items()):
                key.update(_to_bytes(name))
                key.update(_to_bytes(value))

        return key.hexdigest()


    def has_key(self, key):
        """Returns `True` if cache has `key`, `False` otherwise"""
        return key in self.responses


    def __str__(self):
        return 'responses: %s' % (self.responses)



def _to_bytes(s, encoding='utf-8'):
    return s if isinstance(s, bytes) else bytes(str(s), encoding)

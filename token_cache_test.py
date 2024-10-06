import os

from pydeck import settings

from token_cache import TokenCache
import test_settings

TEST_TOKEN: str = "test_token"

def _clean_files():
    try:
        os.remove(test_settings.TEST_TOKEN_CACHE_FILE_NAME)
    except:
        pass

def test_store_token():
    try:
        token_cache = TokenCache(filename=test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        token_cache.put_token(TEST_TOKEN)
        f = open(test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        token = f.read()
        assert token == TEST_TOKEN
    finally:
        _clean_files()

def test_get_token_when_file_does_not_exist():
    try:
        cache = TokenCache(test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        token = cache.get_token()
        assert token is None
    finally:
        _clean_files()

def test_store_and_restore_token():
    try:
        f = open(test_settings.TEST_TOKEN_CACHE_FILE_NAME, "w")
        f.write(TEST_TOKEN)
        f.close()
        token_cache = TokenCache(filename=test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        token = token_cache.get_token()
        assert token == TEST_TOKEN
    finally:
        _clean_files()

def test_update_token():
    try:
        token_cache = TokenCache(filename=test_settings.TEST_TOKEN_CACHE_FILE_NAME)

        token_cache.put_token(TEST_TOKEN)
        assert token_cache.get_token() == TEST_TOKEN

        token_cache.put_token("Another token")
        assert token_cache.get_token() == "Another token"
    finally:
        _clean_files()

def test_clear_cache():
    try:
        cache = TokenCache(test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        cache.put_token(TEST_TOKEN)
        assert cache.get_token() == TEST_TOKEN

        cache.clear_cache()
        assert cache.get_token() is None
    finally:
        _clean_files()

def test_clear_cache_when_cache_is_empty():
    try:
        cache = TokenCache(test_settings.TEST_TOKEN_CACHE_FILE_NAME)
        cache.clear_cache()
    finally:
        _clean_files()

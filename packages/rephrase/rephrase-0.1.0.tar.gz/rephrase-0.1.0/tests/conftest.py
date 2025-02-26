import pytest


@pytest.fixture(scope="session", autouse=True)
def clear_lru_cache():
    """LRU cache cleanup after all tests."""
    yield
    from rephrase.rephraser import rephrase_text

    rephrase_text.cache_clear()

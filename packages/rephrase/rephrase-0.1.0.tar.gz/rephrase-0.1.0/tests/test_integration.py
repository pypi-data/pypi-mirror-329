import os
import time

import pytest
from rephrase.rephraser import STYLE_PROMPTS, rephrase_text

# Skip 'pag walang API key
pytestmark = pytest.mark.skipif(
    os.environ.get("OPENAI_API_KEY") is None,
    reason="OPENAI_API_KEY environment variable not set",
)


@pytest.mark.integration
def test_real_api_call():
    """Test natin sa totoong API, dapat may sagot at iba sa orig!"""
    test_text = "Kumusta ka, mundo!"
    result = rephrase_text(test_text, style="normal")
    assert result
    assert isinstance(result, str)
    assert len(result) > 0
    assert result != test_text


@pytest.mark.integration
@pytest.mark.parametrize("style", list(STYLE_PROMPTS.keys()))
def test_all_styles(style: str) -> None:
    """Subukan natin lahat ng styles sa real API, dapat maangas ang dating!"""
    test_text = "Ang bilis ng fox na tumalon sa tamad na dog, pare!"
    result = rephrase_text(test_text, style=style)
    assert result
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.integration
def test_caching_performance():
    """Check natin yung caching sa totoong API, dapat mabilis 'pag pangalawa!"""
    rephrase_text.cache_clear()  # Linis muna ng cache, para fair!

    test_text = "Testing natin tong caching!"

    start = time.time()
    result1 = rephrase_text(test_text, style="filipino")
    first_call_time = time.time() - start

    start = time.time()
    result2 = rephrase_text(test_text, style="filipino")
    second_call_time = time.time() - start

    assert second_call_time < first_call_time  # Dapat mas mabilis ang pangalawa!
    assert result1 == result2

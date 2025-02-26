import os
from collections.abc import Generator
from typing import Any

import pytest
from openai import OpenAIError
from pytest_mock import MockerFixture
from rephrase.rephraser import (
    STYLE_PROMPTS,
    RephraseError,
    get_client,
    rephrase_text,
)


@pytest.fixture
def setup_env() -> Generator[None]:
    """Setup ng test env with mock API key!"""
    old_key: str | None = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "test_key_bro"
    yield
    # Ibalik sa dati after, no hassle!
    if old_key:
        os.environ["OPENAI_API_KEY"] = old_key
    else:
        del os.environ["OPENAI_API_KEY"]


@pytest.fixture
def mock_openai_response(mocker: MockerFixture) -> Any:
    """Mock natin 'yung OpenAI response, para hindi magastos sa API"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = "Rephrased na 'to, pare!"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_rephrase_text_normal_style(setup_env: None, mock_openai_response: Any) -> None:
    """Test natin 'yung normal style, dapat cool ang labas!"""
    result: str = rephrase_text("Hoy, test lang 'to ha!", style="normal")

    assert result == "Rephrased na 'to, pare!"
    mock_openai_response.chat.completions.create.assert_called_once()


@pytest.mark.parametrize("style", list(STYLE_PROMPTS.keys()))
def test_different_styles(setup_env: None, mocker: MockerFixture, style: str) -> None:
    """Check natin lahat ng styles, from normal to filipino, dapat swabe!"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = f"{style} na 'to, bro!"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    result: str = rephrase_text("Test natin", style=style)
    assert result == f"{style} na 'to, bro!"


def test_empty_text(setup_env: None) -> None:
    """Kung wala kang text, dapat mag-error'"""
    with pytest.raises(RephraseError, match="Wala kang binigay na text"):
        rephrase_text("")


def test_invalid_style(setup_env: None) -> None:
    """Kung wrong ang style, dapat sabihin'"""
    with pytest.raises(RephraseError, match="Wala sa listahan ko"):
        rephrase_text("Test 'to, pare!", style="jejemon")


def test_api_error(setup_env: None, mocker: MockerFixture) -> None:
    """Kung magka-error ang API, GGWP."""
    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.side_effect = OpenAIError("API Down")

    with pytest.raises(RephraseError, match="Hays, sablay sa OpenAI: API Down"):
        rephrase_text("Test 'to, bro!")


def test_unexpected_error(setup_env: None, mocker: MockerFixture) -> None:
    """Kung may random error, sabihin natin 'May glitch, ata!'"""
    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.side_effect = ValueError("Weird Stuff")

    with pytest.raises(RephraseError, match="May glitch ata"):
        rephrase_text("Test 'to, pare!")


def test_get_client_missing_api_key(mocker: MockerFixture) -> None:
    """Magreklamo 'pag walang API key"""

    mocker.patch("rephrase.rephraser._client", None)  # Reset global state
    mocker.patch.dict(os.environ, {}, clear=True)
    with pytest.raises(
        RephraseError, match="Ilagay mo yung OPENAI_API_KEY sa env variable!"
    ):
        get_client()


def test_caching(setup_env: None, mocker: MockerFixture) -> None:
    """Test natin 'yung caching, dapat mabilis sa pangalawa!"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = "Cached na 'to, astig!"

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    rephrase_text.cache_clear()  # Clean slate muna

    result1: str = rephrase_text("Cache test", style="filipino")
    result2: str = rephrase_text("Cache test", style="filipino")

    assert mock_client.chat.completions.create.call_count == 1  # Isa lang dapat
    assert result1 == result2 == "Cached na 'to, astig!"


def test_empty_api_response(setup_env: None, mocker: MockerFixture) -> None:
    """Kung walang sagot ang API, ibalik natin sa orig text"""
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = ""

    mock_client = mocker.patch("rephrase.rephraser._client")
    mock_client.chat.completions.create.return_value = mock_response

    original_text: str = "Test natin 'to, bro!"
    result: str = rephrase_text(original_text)

    assert result == original_text

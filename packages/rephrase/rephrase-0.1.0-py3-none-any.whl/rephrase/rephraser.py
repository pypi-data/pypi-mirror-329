import os
from functools import lru_cache
from typing import Final

from openai import OpenAI, OpenAIError


# Custom exception, Pinoy-style
class RephraseError(Exception):
    """Kung may problema sa rephrasing, sasabihin ko sayo dito!"""

    pass


# Config constants
DEFAULT_MODEL: Final = "gpt-3.5-turbo"  # Solid choice! parang adobo ng AI
DEFAULT_MAX_TOKENS: Final = 150  # Short and sweet
DEFAULT_TEMPERATURE: Final = 0.7  # Sakto lang
DEFAULT_TOP_P: Final = 1.0  # Walang labis, walang kulang
STYLE_PROMPTS: Final[dict[str, str]] = {
    "normal": (
        "Rephrase the following text in a clear, natural way, maintaining its original meaning: '{text}'"
    ),
    "casual": (
        "Rephrase this text in a relaxed, casual tone, like you're chatting with a friend. "
        "Keep it simple and informal: '{text}'"
    ),
    "formal": (
        "Rephrase the following text in a polite, formal tone suitable for professional correspondence. "
        "Ensure the language is respectful and refined: '{text}'"
    ),
    "academic": (
        "Rephrase this text in a precise, academic style, as if it were part of a scholarly article. "
        "Use formal language and avoid contractions or colloquialisms. Example: "
        "'The results are good' becomes 'The findings demonstrate favorable outcomes.' "
        "Text to rephrase: '{text}'"
    ),
    "filipino": (
        "Rephrase this text with a Filipino twist, mixing English and Tagalog in a fun, natural way, "
        "like you're kwentuhan with a barkada. Keep it light and conversational: '{text}'"
    ),
}

# Lazy client - gising lang pag kailangan
_client: OpenAI | None = None


def get_client() -> OpenAI:
    """OpenAI client"""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RephraseError("Ilagay mo yung OPENAI_API_KEY sa env variable!")
        _client = OpenAI(api_key=api_key)
    return _client


# LRU cache para mas tipid sa pag re-rephrase
@lru_cache(maxsize=128)
def rephrase_text(text: str, style: str = "normal", model: str = DEFAULT_MODEL) -> str:
    """
    I-rephrase natin ang text with a style na pasok sa trip ng user ✨!

    Args:
        text: Ano'ng text ang papalitan natin?
        style: Pili ka ng vibe - normal, casual, formal, academic, o filipino.
        model: OpenAI model, default is gpt-3.5-turbo, palag na 'to!

    Returns:
        Rephrased text

    Raises:
        RephraseError: Kung may mali, ipapakita ko agad sayo.
    """
    if not text.strip():
        raise RephraseError("Wala kang binigay na text, bawal ang blanko!")

    if style not in STYLE_PROMPTS:
        raise RephraseError(
            f"Wala sa listahan ko yang '{style}' na yan. Try mo to: {', '.join(STYLE_PROMPTS.keys())}"
        )

    prompt = STYLE_PROMPTS[style].format(text=text)
    client = get_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You're a wordsmith na may Pinoy soul, rephrasing like a pro!",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=DEFAULT_MAX_TOKENS,
            temperature=DEFAULT_TEMPERATURE,
            top_p=DEFAULT_TOP_P,
        )
        result = response.choices[0].message.content
        return result if result else text  # Kung walang laman, balik sa orig na lang
    except OpenAIError as e:
        raise RephraseError(f"Kasalanan ni OpenAI: {e}") from e
    except Exception as e:
        raise RephraseError("May glitch ata 🤤") from e

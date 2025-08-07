from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass(frozen=True)
class Choice:
    value: str
    label: str
    description: str = ""


class TranscriptionModel(str, Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


MODEL_CHOICES: List[Choice] = [
    Choice("tiny", "Tiny", "Muito rápido, menos preciso"),
    Choice("base", "Base", "Equilibrado"),
    Choice("small", "Small", "Boa precisão"),
    Choice("medium", "Medium", "Muito boa precisão (recomendado)"),
    Choice("large", "Large", "Melhor precisão, mais lento"),
]


LANGUAGE_CHOICES: List[Choice] = [
    Choice("pt", "Português"),
    Choice("en", "Inglês"),
    Choice("es", "Espanhol"),
    Choice("fr", "Francês"),
    Choice("de", "Alemão"),
    Choice("it", "Italiano"),
    Choice("auto", "Detecção automática"),
]


def values(choices: List[Choice]) -> List[str]:
    return [c.value for c in choices]


def description_for(choices: List[Choice], value: str) -> str:
    for c in choices:
        if c.value == value:
            return c.description
    return ""



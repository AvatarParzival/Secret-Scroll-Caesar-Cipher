"""Core Caesar cipher functions for Secret Scroll."""


def caesar_cipher(text: str, shift: int) -> str:
    """Return *text* shifted by *shift* positions.

    Uppercase and lowercase ASCII letters are rotated independently. Numbers,
    spaces, punctuation, emoji, and other characters are preserved.
    """
    normalized_shift = shift % 26
    result: list[str] = []

    for character in text:
        if "A" <= character <= "Z":
            result.append(chr((ord(character) - ord("A") + normalized_shift) % 26 + ord("A")))
        elif "a" <= character <= "z":
            result.append(chr((ord(character) - ord("a") + normalized_shift) % 26 + ord("a")))
        else:
            result.append(character)

    return "".join(result)


def encrypt(text: str, shift: int) -> str:
    """Encrypt text using a Caesar shift."""
    return caesar_cipher(text, shift)


def decrypt(text: str, shift: int) -> str:
    """Decrypt text previously encrypted with the same Caesar shift."""
    return caesar_cipher(text, -shift)

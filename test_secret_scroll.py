"""Unit tests for Secret Scroll Caesar Cipher."""

import unittest

from caesar_cipher import decrypt, encrypt


class CaesarCipherTests(unittest.TestCase):
    def test_encrypt_basic_message(self) -> None:
        self.assertEqual(encrypt("Hello, World!", 3), "Khoor, Zruog!")

    def test_decrypt_basic_message(self) -> None:
        self.assertEqual(decrypt("Khoor, Zruog!", 3), "Hello, World!")

    def test_wraps_both_alphabets(self) -> None:
        self.assertEqual(encrypt("xyz XYZ", 3), "abc ABC")

    def test_preserves_non_letters(self) -> None:
        self.assertEqual(encrypt("Python 3.13! 🐍", 5), "Udymts 3.13! 🐍")

    def test_negative_shift(self) -> None:
        self.assertEqual(encrypt("Hello", -1), "Gdkkn")

    def test_large_shift_is_normalized(self) -> None:
        self.assertEqual(encrypt("abc", 29), "def")

    def test_empty_text(self) -> None:
        self.assertEqual(encrypt("", 10), "")

    def test_round_trip(self) -> None:
        original = "Meet me at 10:30 near Gate B."
        for shift in (-53, -1, 0, 1, 13, 26, 99):
            with self.subTest(shift=shift):
                self.assertEqual(decrypt(encrypt(original, shift), shift), original)


if __name__ == "__main__":
    unittest.main()

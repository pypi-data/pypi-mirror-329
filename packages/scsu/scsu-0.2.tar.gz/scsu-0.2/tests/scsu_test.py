import unittest

from src import scsu


class EncodingTest(unittest.TestCase):
    def test_ascii(self):
        s = "Test ASCII string."
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_latin1(self):
        s = "¿Dónde está mi Pokémon, señor?"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_katakana(self):
        s = "ユニコード"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_armenian(self):
        s = "Ի՞նչ է Յունիկոդը"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_hangul(self):
        s = "유니코드에 대해 ?"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_emoji(self):
        s = "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩😪😫😬😭😮😯"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))

    def test_mixture(self):
        s = "犬夜叉が大好きよ。❤️　ワンワン　🐶 Woof woof!"
        self.assertEqual(s, s.encode(scsu.CODEC_NAME).decode(scsu.CODEC_NAME))


class DecodingTest(unittest.TestCase):
    def test_ascii(self):
        b = b"Test ASCII string."
        self.assertEqual(b.decode('ASCII'), b.decode(scsu.CODEC_NAME))

    def test_ascii_quote(self):
        b = b"Form feed or clear screen.\x01\x0C"
        s = b.decode(scsu.CODEC_NAME)
        self.assertEqual(s[-1], "\f")

    def test_window_quote(self):
        b = b"A\x03\x94\x06\x82"
        s = b.decode(scsu.CODEC_NAME)
        self.assertEqual(s, "AДあ")

    def test_unicode_quote(self):
        b = b"Dog \x0E\x72\xAC\x0E\xD8\x3D\x0E\xDC\x36"
        s = b.decode(scsu.CODEC_NAME)
        self.assertEqual(s[-2], "犬")
        self.assertEqual(s[-1], "🐶")

    def test_incomplete_unicode_quote(self):
        b = b"Cat \x0E\x73"
        self.assertRaises(UnicodeDecodeError, b.decode, scsu.CODEC_NAME)

    def test_incomplete_emoji_quote(self):
        b = b"Cat \x0E\xD8\x3D"
        self.assertRaises(UnicodeDecodeError, b.decode, scsu.CODEC_NAME)

    def test_bad_emoji_encoding(self):
        b = b"\x0F\xDE\x3A\xD8\x3D"
        self.assertRaises(UnicodeDecodeError, b.decode, scsu.CODEC_NAME)

    def test_reserved_bytes(self):
        b = b"\x0C"
        self.assertRaises(UnicodeDecodeError, b.decode, scsu.CODEC_NAME)

        b = b"\x0F\xF2"
        self.assertRaises(UnicodeDecodeError, b.decode, scsu.CODEC_NAME)


if __name__ == '__main__':
    unittest.main()

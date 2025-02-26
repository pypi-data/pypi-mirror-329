# Standard Compression Scheme for Unicode

This package implements [SCSU](https://www.unicode.org/reports/tr6/tr6-4.html) as a Python text codec.

## Benefits of Unicode compression

Short strings can be compressed with less overhead than general compression algorithms and with fewer bytes than popular Unicode transformations like [UTF-8](https://en.wikipedia.org/wiki/UTF-8) or [UTF-16](https://en.wikipedia.org/wiki/UTF-16):

* `¿Qué es Unicode?` ("What is Unicode?" in Spanish) is encoded as 18 bytes in UTF-8, but only **16** bytes in SCSU, the same length when encoded in [ISO-8859-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1).
* `ユニコードとは何か？` ("What is Unicode?" in Japanese) is encoded as 30 bytes in UTF-8, 20 bytes in [Shift JIS](https://en.wikipedia.org/wiki/Shift_JIS) and [EUC-JP](https://en.wikipedia.org/wiki/Extended_Unix_Code#EUC-JP), but only **15** bytes in SCSU.
* `𐑢𐑳𐑑 𐑦𐑟 𐑿𐑯𐑦𐑒𐑴𐑛?` ("What is Unicode?" in the [Shavian alphabet](https://en.wikipedia.org/wiki/Shavian_alphabet)) is encoded as 47 bytes in UTF-8, but only **17** bytes in SCSU.

In an extreme case, SCSU can compress long strings of [emoji](https://www.unicode.org/charts/PDF/U1F600.pdf):

```python
emoji = "".join(chr(0x1F600 + n) for n in range(0x50))
sms_data = emoji.encode("UTF-16BE")  # 320 bytes
scsu_data = emoji.encode("SCSU")  # 83 bytes
```

### Requirements

This package requires [Python 3.10](https://docs.python.org/3/whatsnew/3.10.html) or above.

### Usage

Simply import the library and the SCSU codec is ready to use:

```python
import scsu

b = s.encode("SCSU")
```

To automatically add and remove a byte-order mark signature, use `SCSU-SIG` instead of `SCSU`.

### Errata

[CPython bug #79792](https://github.com/python/cpython/issues/79792) causes the sample code (below) to not flush the encoding buffer:

```python
with open(file, mode="w", encoding="SCSU-SIG") as f:
    f.write(s)  # Never flushes the encoding buffer.
```

A workaround is to import the `codecs` module, then replace `open` with `codecs.open`:

```python
import codecs

with codecs.open(file, "w", encoding="SCSU-SIG") as f:
    f.write(s)  # Always flushes the encoding buffer.
```

However, _reading_ an encoded file with the given code will work:

```python
with open(file, mode="r", encoding="SCSU-SIG") as f:
    print(f.read())
```

### Credits

Encoding logic is heavily based on a sample encoder described in "[A survey of Unicode compression](https://www.unicode.org/notes/tn14/UnicodeCompression.pdf)" by Doug Ewell and originally written by Richard Gillam in his book _[Unicode Demystified](https://www.oreilly.com/library/view/unicode-demystified/0201700522/)_, but with some encoding optimizations:
* A two-character lookahead buffer.
  * This avoids a case where switching from Unicode to single-byte mode requires two window switches.
* Compression of sequential static window characters into a single new dynamic window.
  * This avoids a case where a long string of punctuation is encoded as multiple quoted characters. 
* Uses the Latin-1 Supplement window whenever possible.
  * When encoding a string that only contains ASCII and Latin-1 Supplement characters, this results in a string that is both valid in SCSU _and_ ISO-8859-1.

Decoding logic, however, is entirely original.

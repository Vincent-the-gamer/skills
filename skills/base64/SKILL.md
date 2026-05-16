---
name: base64
version: 1.0.0
description: Support encode file/text to base64 and decode base64 to file/text. Use when the user say using base64 to encode/decode file/text.
license: Complete terms in LICENSE.txt
---

# Base64 Usage Guide

## Encode

- Judge the input that user has given：
  - if is a plain string, See [Encode String](#encode-string)
  - else, if is a file, See [Encode File](#encode-file)

Then, send the encoded base64 string or string text file to user.

### Encode String

Use 'scripts/base64_str_encode.py' to encode a string to base64 string.

```bash
python scripts/base64_str_encode.py <str>
```

### Encode File

> [!IMPORTANT]
>
> If base64 string is too long, it will write a base64 string text file, when this happen, send the file to user.

Use 'scripts/base64_file_encode.py' to encode a file to base64 string.

```bash
python scripts/base64_file_encode.py <file_path>
```

## Decode

- Judge the input base64 string that user has given：
  - if it has mime-type, See [Decode File](#decode-file)
  - else, See [Decode String](#decode-string)

Then send the decoded string/file to user.

### Decode String

Use 'scripts/base64_str_decode.py' to decode a base64 string to plain text.

```bash
python base64_str_decode.py <base64_str>
```

### Decode File

Use 'scripts/base64_file_decode.py' to decode base64 string to original file.

```bash
python base64_file_decode.py <base64_str> [output_file]

# or read from file
python base64_file_decode.py -f <encoded_str_text_file_path> [output_file]
```

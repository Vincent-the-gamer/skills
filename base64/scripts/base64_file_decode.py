import base64
import re
import sys


def decode_base64_to_file_with_mimetype(data_uri, output_path):
    """
    解码带MIME类型的Base64字符串并保存文件
    """
    # 1. 使用正则表达式匹配 MIME 和 Base64 数据
    # 格式: data:<mimetype>;base64,<data>
    match = re.match(r"data:(?P<mimetype>.*?);base64,(?P<data>.*)", data_uri)
    if not match:
        raise ValueError("Invalid Base64 Data URI format")

    mimetype = match.group("mimetype")
    data_str = match.group("data")

    # 2. Base64 解码
    file_data = base64.b64decode(data_str)

    # 3. 将二进制数据保存为文件
    with open(output_path, "wb") as f:
        f.write(file_data)

    print(f"File saved: {output_path}")
    print(f"MIME type: {mimetype}")
    return mimetype


def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python base64_file_decode.py <base64_data_uri> [output_file]")
        print(
            "Example: python base64_file_decode.py 'data:text/plain;base64,SGVsbG8gV29ybGQ=' output.txt"
        )
        print("Or from file: python base64_file_decode.py -f data_uri.txt output.pdf")
        sys.exit(1)

    # 处理输入
    if sys.argv[1] == "-f" and len(sys.argv) >= 3:
        # 从文件读取 data_uri
        uri_file = sys.argv[2]
        with open(uri_file, "r", encoding="utf-8") as f:
            data_uri = f.read().strip()
        output_path = sys.argv[3] if len(sys.argv) > 3 else "output.bin"
    else:
        # 直接从命令行参数获取
        data_uri = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "output.bin"

    try:
        decode_base64_to_file_with_mimetype(data_uri, output_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

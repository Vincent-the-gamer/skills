import base64
import sys


def decode_from_base64(encoded_str):
    """将Base64字符串解码为原始字符串"""
    try:
        # 将字符串转换为字节
        bytes_str = encoded_str.encode("utf-8")

        # 进行Base64解码
        decoded_bytes = base64.b64decode(bytes_str)

        # 将解码后的字节转换回字符串
        decoded_str = decoded_bytes.decode("utf-8")

        return decoded_str
    except Exception as e:
        return f"Decoding failed: {e}"


def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python decode.py <base64_string>")
        print("Example: python decode.py 'SGVsbG8gV29ybGQ='")
        sys.exit(1)

    # 获取要解码的Base64字符串
    encoded_str = sys.argv[1]

    # 进行解码
    decoded_str = decode_from_base64(encoded_str)

    # 输出结果
    print(f"Base64 String: {encoded_str}")
    print(f"Decoded: {decoded_str}")


if __name__ == "__main__":
    main()

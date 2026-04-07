import base64
import sys


def encode_to_base64(original_str):
    """将字符串进行Base64编码"""
    # 将字符串转换为字节 (UTF-8)
    bytes_str = original_str.encode("utf-8")

    # 进行Base64编码
    encoded_bytes = base64.b64encode(bytes_str)

    # 将编码后的字节转换回字符串
    encoded_str = encoded_bytes.decode("utf-8")

    return encoded_str


def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python script.py <string_to_encode>")
        print("示例: python script.py 'Hello World'")
        sys.exit(1)

    # 获取要编码的字符串
    original_str = sys.argv[1]

    # 进行编码
    encoded_str = encode_to_base64(original_str)

    # 输出结果
    print(f"编码前: {original_str}")
    print(f"编码后: {encoded_str}")


if __name__ == "__main__":
    main()

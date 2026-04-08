import base64
import mimetypes
import os
import sys


def encode_file_to_base64(file_path):
    """
    将文件转换为带MIME类型的Base64编码字符串
    """
    # 1. 检测文件是否存在
    if not os.path.exists(file_path):
        return None

    # 2. 获取文件格式 (MIME Type)
    mime_type, _ = mimetypes.guess_type(file_path)

    # 如果无法识别文件类型，默认为二进制流
    if not mime_type:
        mime_type = "application/octet-stream"

    # 3. 读取文件并编码
    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    # 4. 拼接 Data URI 格式
    formatted_base64 = f"data:{mime_type};base64,{encoded_string}"

    return formatted_base64


def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python base64_file_encode.py <file_path> [threshold]")
        print("Example: python base64_file_encode.py image.png")
        print(
            "Example: python base64_file_encode.py image.png 500 # Example: Set threshold to 500 characters"
        )
        print(
            "Note: If the encoded string exceeds the threshold, it will be saved to a txt file."
        )
        sys.exit(1)

    file_path = sys.argv[1]

    # 获取阈值（默认200）
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    # 编码文件
    base64_str = encode_file_to_base64(file_path)

    if base64_str is None:
        print(f"Error: File '{file_path}' is not exist.")
        sys.exit(1)

    # 获取文件信息
    file_size = os.path.getsize(file_path)
    mime_type = base64_str.split(";")[0].replace("data:", "")

    print(f"File: {file_path}")
    print(f"MIME Type: {mime_type}")
    print(f"File Size: {file_size} bytes ({file_size / 1024:.2f} KB)")
    print(f"Encoded Length: {len(base64_str)} characters")

    # 检查长度
    if len(base64_str) > threshold:
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = f"{base_name}_base64.txt"

        # 写入文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(base64_str)

        print(
            f"\nEncode result exceeds {threshold} characters, saved to file automatically."
        )
        print(f"Save path: {output_file}")

        # 可选：显示前100个字符预览
        print("\nPreview (first 100 characters):")
        print("-" * 50)
        print(base64_str[:100] + "...")
        print("-" * 50)
    else:
        # 长度不超过阈值，直接打印
        print("\nBase64 Data URI:")
        print("-" * 50)
        print(base64_str)
        print("-" * 50)


if __name__ == "__main__":
    main()

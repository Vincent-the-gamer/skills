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
        print("用法: python base64_file_encode.py <file_path> [阈值]")
        print("示例: python base64_file_encode.py image.png")
        print("示例: python base64_file_encode.py image.png 500  # 设置阈值为500字符")
        print("说明: 超过阈值自动保存到txt文件，默认阈值为200字符")
        sys.exit(1)

    file_path = sys.argv[1]

    # 获取阈值（默认200）
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    # 编码文件
    base64_str = encode_file_to_base64(file_path)

    if base64_str is None:
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)

    # 获取文件信息
    file_size = os.path.getsize(file_path)
    mime_type = base64_str.split(";")[0].replace("data:", "")

    print(f"文件: {file_path}")
    print(f"MIME类型: {mime_type}")
    print(f"文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
    print(f"编码长度: {len(base64_str)} 字符")

    # 检查长度
    if len(base64_str) > threshold:
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = f"{base_name}_base64.txt"

        # 写入文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(base64_str)

        print(f"\n编码结果超过{threshold}字符，已自动保存到文件")
        print(f"保存路径: {output_file}")

        # 可选：显示前100个字符预览
        print("\n预览（前100字符）:")
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

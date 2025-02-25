"""!
@file convert_file_encoding.py
@brief 文件编码转换工具

@details
这个模块提供了文件编码转换的功能，可以：
- 将单个文件从一种编码转换为另一种编码
- 批量转换整个目录下的文件编码
- 支持多种源编码的尝试列表
- 保持目录结构
- 支持文件类型过滤

@author wenqsh
@date 2024-03
@version 1.0

@note
支持的常见编码包括：
- UTF-8
- GB2312
- GBK
- GB18030
等

@example
    # 转换单个文件
    convert_file_encoding("input.txt", "output.txt", "gb2312", "utf-8")
    
    # 转换整个目录
    convert_directory_encoding(
        "src_dir",
        "dst_dir",
        ["gb2312", "gbk"],
        "utf-8",
        [".txt", ".cpp"]
    )
"""
import logging
from pathlib import Path

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('encoding_conversion.log', encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

def convert_file_encoding(input_file, output_file, src_encoding, dst_encoding='utf-8'):
    """!
    @brief 将文件从源编码转换为目标编码
    
    @param input_file 输入文件路径
    @param output_file 输出文件路径
    @param src_encoding 源文件编码，可以是单个编码字符串或编码列表
    @param dst_encoding 目标文件编码，默认为'utf-8'
    
    @return bool 转换是否成功
    """
    # 将字符串格式的编码转换为列表
    encodings = [src_encoding] if isinstance(src_encoding, str) else src_encoding

    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                content = f.read()

            with open(output_file, 'w', encoding=dst_encoding) as f:
                f.write(content)

            logging.info(f"转换成功 - 从 {encoding} 转换到 {dst_encoding} - 文件：{input_file}")
            return True

        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"转换失败 - 文件：{input_file} - 错误：{str(e)}")
            return False
    
    logging.error(f"转换失败 - 无法使用指定的编码读取文件：{input_file}")
    return False

def convert_directory_encoding(
    src_dir: str, 
    dst_dir: str, 
    src_encoding,
    dst_encoding='utf-8',
    extensions: list[str] = None
):
    """!
    @brief 递归遍历源文件夹中的所有文件，将符合后缀名要求的文件进行编码转换并保持相对路径复制到目标文件夹

    @param src_dir 源目录路径
    @param dst_dir 目标目录路径
    @param src_encoding 源文件编码（支持单个编码或编码列表）
    @param dst_encoding 目标文件编码，默认为'utf-8'
    @param extensions 要处理的文件扩展名列表（例如['.txt', '.cpp']），None表示处理所有文件

    @note
    - 会自动创建目标目录结构
    - 跳过无法识别的文件编码
    - 保留原始文件时间戳

    @return tuple 包含成功和失败计数的元组 (success_count, fail_count)
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    
    logging.info(f"开始处理目录：{src_dir} -> {dst_dir}")
    logging.info(f"源编码：{src_encoding}，目标编码：{dst_encoding}")
    if extensions:
        logging.info(f"处理的文件类型：{', '.join(extensions)}")
    
    success_count = 0
    fail_count = 0
    
    try:
        dst_path.mkdir(parents=True, exist_ok=True)
        
        for src_file in src_path.rglob('*'):
            if src_file.is_dir():
                continue
                
            if extensions and src_file.suffix.lower() not in extensions:
                continue
                
            rel_path = src_file.relative_to(src_path)
            dst_file = dst_path / rel_path
            
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            if convert_file_encoding(str(src_file), str(dst_file), src_encoding, dst_encoding):
                success_count += 1
            else:
                fail_count += 1
                
        logging.info(f"目录处理完成 - 成功：{success_count}个文件，失败：{fail_count}个文件")
        
    except Exception as e:
        logging.error(f"目录处理异常 - {str(e)}")

# 使用示例：
if __name__ == '__main__':
    # 转换单个文件的示例
    # name = "FloorFinding"
    # ext = ".h"
    # input_file = f"temp/{name}{ext}"
    # output_file = f"temp/{name}{ext}"
    # convert_file_encoding(input_file, output_file, ['gb2312', 'gbk'], 'utf-8')
    
    # 转换整个目录的示例
    src_directory = r"C:\Users\wenqsh\Desktop\dblfu_2"
    dst_directory = r"C:\Users\wenqsh\Desktop\dblfu_3"
    file_extensions = ['.h', '.cpp', '.hpp', '.cu', '.cuh']  # 指定要处理的文件类型
    src_encodings = ['utf-8', 'gb2312', 'gbk', 'gb18030']  # 可能的源文件编码列表
    dst_encodings = 'gb2312'  # 目标文件编码
    convert_directory_encoding(
        src_directory, 
        dst_directory, 
        src_encodings,
        dst_encodings,
        file_extensions
    ) 
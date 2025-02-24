
"""!
@file copy_files.py
@brief 文件复制工具

@details
这个模块提供了文件复制功能，可以：
- 按文件后缀名过滤要复制的文件
- 将源目录中的文件复制到目标目录
- 保持原有的目录结构
- 支持多种文件类型的批量复制
- 自动创建必要的目标子目录

@author wenqsh
@date 2024-03
@version 1.0

@note
特性说明：
- 支持路径对象(Path)或字符串路径作为输入
- 支持带点或不带点的后缀名（如 '.txt' 或 'txt'）
- 后缀名匹配不区分大小写
- 使用 shutil.copy2 保留文件元数据

@example
    # 复制所有Python和C++文件
    copy_files_with_extensions(
        source_dir='./src',
        target_dir='./backup',
        extensions=['.py', '.cpp']
    )
"""
from pathlib import Path
import shutil
from typing import List

def copy_files_with_extensions(
    source_dir: Path | str,
    target_dir: Path | str,
    extensions: List[str]
) -> None:
    """!
    @brief 将源目录中指定后缀名的文件复制到目标目录，保持相对路径结构
    
    @param source_dir 源目录的路径
    @param target_dir 目标目录的路径
    @param extensions 需要复制的文件后缀名列表
    
    @return None
    
    @details
    遍历源目录中的所有文件，如果文件后缀名在指定列表中，
    则将其复制到目标目录中对应的相对路径位置
    """
    # 转换为Path对象
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    
    # 确保后缀名都以.开头
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    # 遍历源目录中的所有文件
    for source_file in source_dir.rglob('*'):
        # 只处理文件（跳过目录）
        if source_file.is_file() and source_file.suffix.lower() in extensions:
            # 计算相对路径
            rel_path = source_file.relative_to(source_dir)
            
            # 计算目标文件路径
            target_file = target_dir / rel_path
            
            # 创建目标目录（如果不存在）
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            shutil.copy2(source_file, target_file)
            print(f"已复制: {source_file} -> {target_file}")

# 使用示例
if __name__ == '__main__':
    # 定义参数
    source_path = r"D:\project\vs2015\dblfu_v\dblfu"
    target_path = r"C:\Users\wenqsh\Desktop\dblfu_2"
    file_extensions = ['.c', '.cpp', '.h', '.hpp', '.cu', '.cuh', '.hpp']
    
    # 复制文件
    copy_files_with_extensions(
        source_dir=source_path,
        target_dir=target_path,
        extensions=file_extensions
    ) 
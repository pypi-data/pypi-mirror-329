# hjimi_tools

## Installation

### Prerequisites

Before installing `hjimi_tools`, ensure that you have Python 3.8 or a higher version installed on your system. You can check your Python version by running the following command in your terminal:

```bash
python --version
```
### Installation Steps
To install `hjimi_tools`, you can use `pip`, the Python package installer. Open your terminal and execute the following command:
```bash
pip install hjimi-tools
```
This command will download and install the latest version of hjimi_tools and its dependencies from the Python Package Index (PyPI). If you want to install a specific version of hjimi_tools, you can specify the version number like this:

```bash
pip install hjimi-tools==<version_number>
```
Replace <version_number> with the actual version you want to install.

### Verifying the Installation
After the installation is complete, you can verify that hjimi_tools is installed correctly by importing it in a Python script or interactive session. Open a Python interpreter and try the following:
```python
import hjimi_tools
```
If there are no errors, it means that `hjimi_tools` has been successfully installed and is ready to be used. You can now start using the various utilities provided by `hjimi_tools` in your Python projects.

## Python Package Setup Script

This script is a utility for automatically setting up a new Python package structure. It creates a directory structure for the package, as well as several important files such as `pyproject.toml`, `README.md`, `LICENSE`, and `requirements.txt`.

### Parameters

- `-p`, `--package_name`: (str) The name of the package to set up. This is a required argument.
- `-v`, `--version`: (str, optional) The version of the package. Defaults to '0.0.1'.
- `-d`, `--description`: (str, optional) A brief description of the package. Defaults to 'A small example package'.
- `-a`, `--author`: (str, optional) The name of the author. Defaults to 'Example Author'.
- `-e`, `--author_email`: (str, optional) The email of the author. Defaults to 'author@example.com'.
- `-u`, `--homepage`: (str, optional) The homepage URL of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY'.
- `-b`, `--bug_tracker`: (str, optional) The URL for the bug tracker of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues'.
- `-r`, `--requirements`: (str, optional) List of package requirements. Multiple packages can be specified separated by spaces.

### Usage

To use this script, you simply need to run it with Python and pass the name of the package you want to create as a command line argument. For example:

```bash
python setup_package.py --package_name my_new_package
```
or 

```bash
# 在你的应用中
from hjimi_tools import PackageSetup

# 创建一个新的 Python 包结构
package_setup = PackageSetup(package_name='my_new_package', version='1.0.0')
package_setup.setup_package()

```

This will create a new directory called `hjimi_tools` with the following structure:

```
my_new_package/
├── src/
│   └── my_new_packages/
│       └── __init__.py
├── test/
├── pyproject.toml
├── README.md
├── LICENSE
└── requirements.txt
```

### Command Line Arguments

The script accepts several command line arguments for customizing the package:

- `package_name`: The name of the package to set up. This is a required argument.
- `--version`: The version of the package. Defaults to '0.0.1'.
- `--description`: The description of the package. Defaults to 'A small example package'.
- `--author`: The author of the package. Defaults to 'Example Author'.
- `--author_email`: The email of the author. Defaults to 'author@example.com'.
- `--homepage`: The homepage URL of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY'.
- `--bug_tracker`: The bug tracker URL of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues'.

### Requirements

This script requires Python 3.8 or higher.
---

## C Project Generator

This Python class, `CProjectGenerator`, is a utility for automatically setting up a new C project structure. It creates a directory structure for the project, as well as several important files such as `main.c`, `Makefile` or `CMakeLists.txt` depending on the chosen build system.

### Class Initialization

The `CProjectGenerator` class is initialized with the following parameters:

- `project_name`: The name of the project to set up. This is a required argument.
- `modules`: The names of the modules to be created. This is an optional argument and defaults to an empty string.
- `build_system`: The build system to use. This can be either 'make' or 'cmake'. Defaults to 'make'.

Example:

```python
gen = CProjectGenerator("my_project", "module1 module2", "cmake")
```

##3 Directory Structure

The following directory structure will be created:

```
my_project/
├── src/
│   └── main.c
├── include/
├── lib/
├── bin/
├── obj/
├── test/
└── docs/
```

### Generated Files

The class will generate a `main.c` file in the `src/` directory as well as a `Makefile` or `CMakeLists.txt` in the project root directory depending on the chosen build system. If modules are specified, corresponding `.c` and `.h` files will be created in the `src/` and `include/` directories respectively.

### Parameters
- `project_name`: (str) The name of the project to set up. This is a required argument.
- `-b` or `--build`: (str, optional) The build system to use. It can either be 'make' or 'cmake'. The default is 'make'.
- `-m` or `--modules`: (str, optional) A comma-separated list of module names. These modules will have corresponding `.c` and `.h` files created. If not specified, no modules will be created.


### Usage

To use this class to generate a project, you simply need to create an instance of the class and call the `generate_project` method. For example:

```python
gen = CProjectGenerator("my_project", "module1,module2", "cmake")
gen.generate_project()
```

This will create a new project with the specified name, modules and build system.


## File Collector

The FileCollector class is a utility designed to collect files with specific extensions from a list of given paths, recursively traverse directories to find these files, and write their contents into a Markdown file formatted with code blocks. It supports multiple file types, automatically determining the appropriate syntax highlighting for each based on the file extension, such as Python for .py files or JavaScript for .js files. The class handles multiple root directories and organizes the output by grouping files under their respective project root directories, using top-level headings for each project and secondary headings for each file. It writes the relative paths of the files, followed by their content in a code block, allowing users to document code and other text files in a structured and easily readable format. Additionally, it gracefully handles potential encoding errors when reading files by including an error message in the output. The entire process is executed through the run method, which first collects the files and then generates the Markdown output, ensuring the resulting file is ready for documentation or sharing purposes.

### Parameters
- `paths`: List of file or directory paths to collect files from.
- `extensions`: List of file extensions to collect.
- `output_path`: Path to the output markdown file.

### Usage

```python
from hjimi_tools import FileCollector

# Initialize FileCollector, specify the paths, file extensions and output_path to collect
collector = FileCollector(paths=['/path/to/project'], extensions=['.py', '.md', '.txt'], output_path="output.md")

# Collect the files and save their content to a specified Markdown file
collector.run()
```

## File Encoding Converter

### Features
- 支持单个文件或整个目录的编码转换
- 自动检测源文件编码（支持编码尝试列表）
- 保持目录结构不变
- 支持多种目标编码格式（UTF-8/GBK/GB2312等）
- 详细的日志记录和错误处理

### 参数说明
```python
convert_directory_encoding(
    src_dir: str,          # 源目录路径
    dst_dir: str,          # 目标目录路径  
    src_encoding,          # 源编码（支持列表形式尝试多种编码）
    dst_encoding='utf-8',  # 目标编码（默认UTF-8）
    extensions: list[str] = None  # 指定处理的后缀名列表
)
```

### 使用示例
```python
from hjimi_tools import convert_directory_encoding

# 转换整个目录编码
convert_directory_encoding(
    src_dir="source_folder",
    dst_dir="converted_folder",
    src_encoding=['gb2312', 'gbk'],
    dst_encoding='utf-8',
    extensions=[".h", ".cpp", ".txt"]
)
```

## File Copy Utility

### 功能特性
- 按文件后缀名过滤复制
- 保持原始目录结构
- 自动创建目标目录
- 保留文件元数据
- 支持批量操作

### 核心方法
```python
copy_files_with_extensions(
    source_dir: Path | str,  # 源目录路径
    target_dir: Path | str,  # 目标目录路径
    extensions: List[str]     # 要复制的文件后缀列表
)
```

### 使用示例
```python
from hjimi_tools import copy_files_with_extensions

# 复制指定类型文件
copy_files_with_extensions(
    source_dir="/path/to/source",
    target_dir="/path/to/target",
    extensions=['.py', '.cpp', '.h']
)
```

## License

MIT License

## Contact

- Author: wenquanshan
- Email: wenquanshan@sximi.com
- Project Homepage: https://github.com/zidanewenqsh/pdf_processor
- Issue Tracking: https://github.com/zidanewenqsh/pdf_processor/issues

## Version History

### 0.0.5
- Initial release
- Basic Python package structure generation
- C project structure generation
- File collector functionality

### 0.1.0 
- Added short format support for command line arguments:
  - `-p` for `--package_name`
  - `-v` for `--version`
  - `-d` for `--description`
  - `-a` for `--author`
  - `-e` for `--author_email`
  - `-u` for `--homepage`
  - `-b` for `--bug_tracker`
  - `-r` for `--requirements`
- Added requirements parameter support:
  - Directly specify project dependencies via command line
  - Support multiple space-separated dependencies
  - Automatically write dependencies to pyproject.toml and requirements.txt

### 0.1.1
- Added file encoding conversion tool module
- Added intelligent file copy utility
- Enhanced exception handling for directory processing
- Improved cross-platform path compatibility

### 0.1.2 (Latest)
- Renamed convert_file_encoding to convert_file_encoder
- Fixed module import issues
- Improved documentation
- Enhanced code stability
- Added `__version__` attribute for version checking
#!/usr/bin/env python
# coding=utf-8
import datetime
import os


class CProjectGenerator:
    def __init__(self, project_name, modules="", build_system="make", delimiter=","): 
        assert build_system in ["make", "cmake"]
        self.project_name = project_name
        self.build_system = build_system
        self.modules = modules
        self.delimiter = delimiter
        # 创建示例源文件和头文件
        self.source_files = {
            f"{project_name}/src/main.c": """#include "stdio.h"
int main() {
    return 0;
}
"""
        }

    def get_prefix(self, file):
        now = datetime.datetime.now()
        metadata = {
            'Author': 'wenquanshan',
            'License': 'MIT',
            'Description': 'xxx',
            'File': os.path.basename(file),
            'Date': now.strftime("%Y-%m-%d"),
            'Time': now.strftime("%H:%M:%S"),
        }

        prefix = f"""/*
 * @file {file}
 * @date {metadata['Date']}
 * @time {metadata['Time']}
 * @author {metadata['Author']}
 * @license {metadata['License']}
 * @description {metadata['Description']}
 */
"""
        return prefix

    def __generate_directory_structure(self):
        for subdir in [
            f"{self.project_name}/src",
            f"{self.project_name}/include",
            f"{self.project_name}/lib",
            f"{self.project_name}/bin",
            f"{self.project_name}/obj",
            f"{self.project_name}/test",
            f"{self.project_name}/docs",
        ]:
            if not os.path.exists(subdir):
                os.makedirs(subdir)

    def __create_modules_files(self):
        if self.modules == "":
            return
            
        self.modules = self.modules.split(self.delimiter)
        self.modules = [module.strip() for module in self.modules]
        self.modules = [module for module in self.modules if module != ""]
        
        for module in self.modules:
            prefix = self.get_prefix(module)
            source_path = f"{self.project_name}/src/{module}.c"
            header_path = f"{self.project_name}/include/{module}.h"
            if not os.path.exists(source_path):
                with open(source_path, "w") as f:
                    f.write(f"{prefix}\n")
                    f.write(f"""#include "{module}.h"
// {module} functions
""")
            if not os.path.exists(header_path):
                with open(header_path, "w") as f:
                    f.write(f"{prefix}\n")
                    f.write(f"""#ifndef {module.upper()}_H
#define {module.upper()}_H
// {module} declarations
#endif
""")

    def __create_examples_files(self):
        for file_path, content in self.source_files.items():
            prefix = self.get_prefix(os.path.basename(file_path))
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "w") as f:
                f.write(f"{prefix}\n")
                f.write(content)

    def __create_build_system_file(self):
        if self.build_system == 'make':
            if not os.path.exists(f"{self.project_name}/Makefile"):
                makefile_content = f"""CC=gcc
CFLAGS=-g -Wall -Wl,-rpath,. -Iinclude
LDFLAGS=-Llib
SRC_DIR=src
OBJ_DIR=obj
BIN_DIR=bin

SOURCES=$(wildcard $(SRC_DIR)/*.c)
OBJECTS=$(SOURCES:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
TARGET=$(BIN_DIR)/{self.project_name}

all: $(TARGET)

$(TARGET): $(OBJECTS)
\t$(CC) $(LDFLAGS) $^ -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
\t$(CC) $(CFLAGS) -c $< -o $@

clean:
\trm -f $(OBJ_DIR)/*.o $(TARGET)

.PHONY: all clean
"""
                with open(f"{self.project_name}/Makefile", "w") as f:
                    f.write(makefile_content)
        elif self.build_system == 'cmake':
            if not os.path.exists(f"{self.project_name}/CMakeLists.txt"):
                cmakelists_content = """cmake_minimum_required(VERSION 3.10)

# 设置项目名称和版本
project({self.project_name} VERSION 1.0)

# 指定 C 标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

# 设置默认构建类型为 Debug
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()

# 设置输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)

# 添加可执行文件
add_executable(${{PROJECT_NAME}} src/main.c)

# 设置调试和发布特定的编译器标志
target_compile_options(${{PROJECT_NAME}} PRIVATE
  $<$<CONFIG:Debug>:-g>
  $<$<CONFIG:Release>:-O3>
)

install(TARGETS ${{PROJECT_NAME}} DESTINATION bin)
"""
                with open(f"{self.project_name}/CMakeLists.txt", "w") as f:
                    f.write(cmakelists_content)

    def generate_project(self):
        self.__generate_directory_structure()
        self.__create_modules_files()
        self.__create_examples_files()
        self.__create_build_system_file()
        print(f"{self.project_name} project generated successfully.")

def parse_arguments():
    import argparse
    # 创建解析器
    parser = argparse.ArgumentParser(
        description='Create a C project directory structure with Makefile or CMakeLists.txt.')
    # 添加项目名称参数
    parser.add_argument('project_name', type=str, help='The name of the project')
    # 添加构建系统选择参数
    parser.add_argument('-b', '--build', type=str, choices=['make', 'cmake'], default='make',
                        help='The build system to use (default: make)')
    # 添加模块名称列表参数
    parser.add_argument('-m', '--modules', type=str, default="",
                        help='Comma-separated list of module names to create .c and .h files for')

    # 解析命令行参数
    args = parser.parse_args()
    return args

def test():
    args = parse_arguments()
    package_setup = CProjectGenerator( args.project_name, args.modules, args.build)
    package_setup.generate_project()

if __name__ == "__main__":
    test()


#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This script sets up the package structure for a new Python package.

Usage:
    python setup_package.py --package_name <package_name>

Example:
    python setup_package.py --package_name my_package

"""
import os

class PackageSetup:
    def __init__(self, package_name, version='0.0.1', description='A small example package',
                 author='Example Author', author_email='author@example.com',
                 homepage='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY',
                 bug_tracker='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues',
                 requirements=None):
        self.package_name = package_name
        self.version = version
        self.description = description
        self.author = author
        self.author_email = author_email
        self.homepage = homepage
        self.bug_tracker = bug_tracker
        self.requirements = requirements or []

    @staticmethod
    def __create_file(path, content=''):
        if not os.path.isfile(path):
            with open(path, 'w') as f:
                f.write(content)
        else:
            print(f"File {path} already exists.")

    @staticmethod
    def __create_dir(path):
        if not os.path.isdir(path):
            os.makedirs(path)
        else:
            print(f"Directory {path} already exists.")

    def setup_package(self):
        # Create the src directory to hold the package
        src_dir = os.path.join(self.package_name, 'src')
        package_dir = os.path.join(src_dir, self.package_name)
        self.__create_dir(package_dir)
        # Create the test directory to hold the test script
        test_dir = os.path.join(self.package_name, "test")
        self.__create_dir(test_dir)
        # Create empty __init__.py
        self.__create_file(os.path.join(package_dir, '__init__.py'))

        # Create pyproject.toml file with dynamic content
        requires_list = ['setuptools>=42', 'wheel'] + self.requirements
        requires_str = ', '.join(f'"{req}"' for req in requires_list)
        
        pyproject_content = f"""[build-system]
requires = [{requires_str}]
build-backend = "setuptools.build_meta"

[project]
name = "{self.package_name}"
version = "{self.version}"
authors = [
{{ name = "{self.author}", email = "{self.author_email}" }},
]
description = "{self.description}"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    {', '.join(f'"{req}"' for req in self.requirements)}
]

[project.urls]
"Homepage" = "{self.homepage}"
"Bug Tracker" = "{self.bug_tracker}"

"""
        self.__create_file(os.path.join(self.package_name, 'pyproject.toml'), pyproject_content)

        # Create README.md file
        self.__create_file(os.path.join(self.package_name, 'README.md'), f'# {self.package_name}\n')

        # Create LICENSE file
        self.__create_file(os.path.join(self.package_name, 'LICENSE'), 'MIT License\n')

        # Create requirements.txt file
        requirements_content = '\n'.join(self.requirements)
        self.__create_file(os.path.join(self.package_name, 'requirements.txt'), requirements_content)

        print(f"Package {self.package_name} structure has been set up.")


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Set up a Python package structure.')
    parser.add_argument('-p', '--package_name', type=str, default='python_project_demo', help='The name of the package to set up')
    parser.add_argument('-v', '--version', type=str, default='0.0.1', help='The version of the package')
    parser.add_argument('-d', '--description', type=str, default='A small example package', help='The description of the package')
    parser.add_argument('-a', '--author', type=str, default='Example Author', help='The author of the package')
    parser.add_argument('-e', '--author_email', type=str, default='author@example.com', help='The email of the author')
    parser.add_argument('-u', '--homepage', type=str, default='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY', help='The homepage URL of the package')
    parser.add_argument('-b', '--bug_tracker', type=str, default='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues', help='The bug tracker URL of the package')
    parser.add_argument('-r', '--requirements', type=str, nargs='*', help='List of package requirements')
    return parser.parse_args()

def test():
    args = parse_arguments()
    package_setup = PackageSetup(
        package_name=args.package_name,
        version=args.version,
        description=args.description,
        author=args.author,
        author_email=args.author_email,
        homepage=args.homepage,
        bug_tracker=args.bug_tracker,
        requirements=args.requirements
    )
    package_setup.setup_package()

if __name__ == "__main__":
    test()

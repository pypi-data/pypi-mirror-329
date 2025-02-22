from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path

README = "README.md"
this_directory = Path(__file__).parent
long_description = (this_directory / README).read_text(encoding='utf-8')
# fileMapping
print("\033[1;32m Start installing fileMapping \033[0m")
try:
    setup(
        name='fileMapping',
        version='0.3.16',
        author='朝歌夜弦',
        author_email='bop-lp@qq.com',
        description='用于快速调用文件夹下的py文件或者包',
        long_description = long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/bop-lp/fileMapping",
        packages=find_packages(),
        install_requires=[]
    )
except Exception as e:
    print(f"Installation failed! \n\033[1;31m ×\033[0m Please check the error message: \n\t\033[1;31m╰─>\033[0m\n\033[1;31m{e}\033[0m")

print("\033[1;32m Installation successful! \nThank you for using, if you have any questions please contact the author: bop-lp@qq.com \033[0m")


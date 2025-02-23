# coding:utf-8
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# here = path.abspath(path.dirname(__file__))

# # Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name="AutoTrans",
    version="2025.02.22",
    keywords = ['LLM', 'chatgpt', 'translation', 'automator'],
    description = 'Automating the entire translation process with LLM',
    author = 'Jinbiao Yang',
    author_email = 'ray306@gmail.com',
    install_requires = ['pandas', 'jinja2', 'fastapi', 'deepl', 'nltk', 'pyperclip', 'uvicorn', 'toml', 'langchain','langchain_openai'],

    packages=find_packages(
        exclude=['__pycache__', '.git', 'config.txt'] 
    ),
    # package_dir={'': 'AutoTrans'},  # 指定AutoTrans为根目录
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'autotrans=AutoTrans.cli:run_uvicorn', # 生成一个可执行命令行的文件
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
    ],
)

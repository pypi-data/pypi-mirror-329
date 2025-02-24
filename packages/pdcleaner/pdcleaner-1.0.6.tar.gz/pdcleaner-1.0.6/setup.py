from setuptools import setup, find_packages

setup(
    name='pdcleaner',
    version='1.0.6',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    description='修复了功能：新增将None替换成空字符串',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://gitee.com/manjim/pdcleaner',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='txhyy',
    version='0.1.0',
    description='txhyy',
    long_description=long_description,
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=find_packages(),
    package_data={
        'txhyy': ['*.pyd'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'txzhushi=txhyy.txzhushi:main', 
            'txbook=txhyy.txbook:main', 
            'txfz=txhyy.txfz:main', 
            'txtree=txhyy.txtree:main', 
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        "PyQt6",
        "moviepy==1.0.3",
        "uncompyle6",
        "pysrt",
        "pillow",
        "fonttools",
        "wmi",
        "pywin32",
        "cryptography",
        "codinghou",
    ],
)
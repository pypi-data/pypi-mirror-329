from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='txhyy',
    version='0.0.6',
    description='txhyy',
    long_description=long_description,
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=find_packages(),
    package_data={
        'txhyy': ['*.pyd'],
        'txhyy': ['*.pyi'],
        'txhyy': ['*.ico'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'txzhushi=txhyy.txzhushi:main', 
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        "PyQt6",
        "moviepy==1.0.3",
        "uncompyle6",
        "pysrt",
        "pillow",
    ],
)
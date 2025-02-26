from setuptools import setup, find_packages

setup(
    name="file_compressor",
    version="0.1.0",
    description="A simple tool to compress files and directories into zip archives",
    author="Your Name",
    author_email="srimathisundar10@gmail.com",
    url="https://github.com/Srimathi10/file_compressor",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'compress-file=file_compressor.file_compressor:compress_file',
            'compress-dir=file_compressor.file_compressor:compress_directory'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

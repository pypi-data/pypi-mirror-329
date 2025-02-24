from setuptools import setup, find_packages

setup(
    name="file_structure_creator",
    version="1.0.0",
    description="根据文件描述创建目录结构的小工具",
    author="易源",
    author_email="zjxfly@126.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "create-structure=file_structure_creator.creator:main",
        ],
    },
    install_requires=[],  # 如果有依赖项，可以在这里添加
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
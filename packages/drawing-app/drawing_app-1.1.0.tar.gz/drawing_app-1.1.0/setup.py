from setuptools import setup, find_packages

setup(
    name="drawing_app",  # 模块名称
    version="1.1.0",  # 版本号
    author="Your Name",  # 作者
    author_email="your.email@example.com",  # 作者邮箱
    description="A simple drawing application and image viewer.",  # 简短描述
    long_description=open("README.md").read(),  # 从 README.md 读取长描述
    long_description_content_type="text/markdown",  # 长描述格式
    url="https://github.com/yourusername/drawing_app",  # 项目主页（可选）
    packages=find_packages(),  # 自动发现包和子包
    install_requires=["pygame"],  # 依赖项
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python 版本要求
    entry_points={
        "console_scripts": [
            "drawing_app=drawing.main:main",  # 定义命令行入口
        ],
    },
    include_package_data=True,  # 包含非代码文件
    package_data={"": ["*.py", "*.jpg"]},  # 包含的文件类型
)
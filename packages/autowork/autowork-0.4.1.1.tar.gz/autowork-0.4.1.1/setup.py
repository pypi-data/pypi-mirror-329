from setuptools import setup, find_packages

setup(
    name="autowork",
    version="0.4.1.1",
    packages=find_packages(),
    install_requires=[
        # List dependencies here, e.g.,
        # "requests",
        # "numpy"
    ],
    author="Yingjie Wei",
    author_email="yingjie.wei@qq.com",
    description="autowork to automatically process the task (write code and execute it) based on LLM.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yingjiewei/autowork",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

from setuptools import setup, find_packages

setup(
    name="hybridtffs",  # Tên package trên PyPI
    version="0.1.5",  # Phiên bản đầu tiên
    author="kieuanh",
    author_email="vukieuanh.hnue@gmail.com",
    description="Mo ta ngan",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VuKieuAnh/hybrid-tffs.git",  # Link repo (nếu có)
    packages=find_packages(),  # Tự động tìm package trong thư mục
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.2",
        "mlxtend>=0.19.0",
        "tffs"
    ],
)
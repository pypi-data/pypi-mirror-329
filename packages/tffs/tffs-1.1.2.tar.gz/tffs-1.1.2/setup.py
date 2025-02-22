from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="tffs",                 # Tên thư viện
    version="1.1.2",                   # Phiên bản
    description="Feature selection based on top frequency",  # Mô tả
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vu Kieu Anh",                # Tên tác giả
    author_email="vukieuanh.hnue@gmail.com",  # Email tác giả
    url="https://github.com/VuKieuAnh/pypi-tffs",  # URL GitHub (nếu có)
    packages=find_packages(),          # Tự động tìm kiếm package
    classifiers=[                      # Phân loại thư viện
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',           # Phiên bản Python yêu cầu
    install_requires=[
        "numpy>=1.21.0",
        "scikit-learn>=1.0.2"
    ],
)
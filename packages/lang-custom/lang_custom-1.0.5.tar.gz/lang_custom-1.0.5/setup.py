from setuptools import setup, find_packages

setup(
    name="lang_custom",
    version="1.0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    description="A simple language manager for loading translations from JSON files.",
    author="Gấu Kẹo",
    author_email="maicutewa2007@gmail.com",
    url="https://github.com/GauCandy/lang_custom",
    license="MIT",
    license_files=("LICENSE",),  # Đảm bảo file LICENSE được bao gồm khi đóng gói
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

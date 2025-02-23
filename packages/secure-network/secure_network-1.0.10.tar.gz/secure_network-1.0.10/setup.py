from setuptools import setup, find_packages

setup(
    name="secure_network",
    version="1.0.10",
    author="Neo Zetterberg",
    author_email="20091103neo@gmail.com",
    description="A secure networking extension with authentication, HMAC, and encryption.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NeoZett/SecureNetwork",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "bcrypt",
        "pyotp",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
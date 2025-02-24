from setuptools import setup, find_packages

setup(
    name="cipher-lab",  # Changed to desired package name
    version="0.1.2",  # Increment version
    packages=find_packages(),
    package_data={
        'cipher_package': ['cipher_code/*/*.py'],
    },
    entry_points={
        'console_scripts': [
            'get_all=cipher_package.cli:main',  # Unified command
        ],
    },
    author="Your Name",
    author_email="your@email.com",
    description="Classic cipher implementations with export functionality",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cipher-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="ciphers cryptography encryption decryption",
)
from setuptools import setup, find_packages

setup(
    name="sipher-lab",
    version="0.1.1",
    packages=find_packages(),
    package_data={
        'sipher_package': ['cipher_code/*/*.py'],  # Changed package name
    },
    entry_points={
        'console_scripts': [
            'get_siphers=sipher_package.cli:main',  # Changed command name
        ],
    },
    install_requires=[
        'setuptools>=68.0.0',
    ],
    author="Your Name",
    author_email="your@email.com",
    description="Classic cipher implementations including Vernam cipher",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sipher-lab",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="ciphers cryptography vernam encryption",
)
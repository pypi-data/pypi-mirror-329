from setuptools import setup, find_packages

setup(
    name="aitronos-cli",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[
        "click>=7.0",
        "pytest>=6.0.0",
    ],
    entry_points={
        'console_scripts': [
            'aitronos=aitronos_alpha.cli:main',
        ],
    },
    author="Phillip Loacker",
    author_email="phillip.loacker@aitronos.com",
    description="A command-line interface tool for streamlining AI development workflows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Freddy-Development/Aitronos-CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
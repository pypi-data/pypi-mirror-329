from setuptools import setup, find_packages

setup(
    name="KgmiColors",
    version="0.1.0",
    description="Un package simple pour colorer les textes dans la console.",
    author="Kagami",
    url="https://github.com/Uwu-Kagami",
    packages=find_packages(),
    readme = "README.md",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.25.1,<3.0.0"
    ]
)


from setuptools import setup, find_packages

setup(
    name="GraphiteInter",
    version="0.2.6",
    description="A simple GUI framework with tkinter for creating interactive interfaces.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Leonardo",
    author_email="leonardonery616@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Pillow",  # Dependência que você está usando
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="augmentimg",
    version="1.1.7",  # Increment the version to 1.1.7
    description="A simple no-code tool to augment Images and Annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pillow==9.5.0",
        "torch==2.2.1",
        "torchvision==0.17.1",
        "PyQt5>=5.15.4,<6",
        "numpy>=1.21.0,<1.26.0",
        "opencv-python>=4.5.0,<4.9.0",
        "albumentations>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "augment-img = augmentimg.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # Mark as stable
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

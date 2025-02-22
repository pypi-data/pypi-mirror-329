from setuptools import setup, find_packages
 

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()


setup(
    name="augmentimg",
    version="1.1.4",
    description="A simple no-code tool to augment Images and Annotations",
    packages=find_packages(),
    install_requires=[
        "pillow==9.5.0",
        "torch==2.2.1",
        "torchvision==0.17.1",
        "PyQt5>=5.15.4,<6",  # Allows minor version updates
        "numpy>=1.21.0,<1.26.0",
        "opencv-python>=4.5.0,<4.9.0",
        "albumentations>=1.3.0",
    ],

    entry_points={
        "console_scripts": [
            "augment-img = augmentimg.main:main",
        ],
    },
    long_description="A simple no-code tool to augment Images and Annotations",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

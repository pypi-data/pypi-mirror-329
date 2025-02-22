from setuptools import setup, find_packages

# Read version from version.py
with open("mamasight/version.py", "r") as f:
    exec(f.read())

# Read long description from README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mamasight",
    version=__version__,
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility for screen parsing and analysis using YOLO and OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mamasight",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/mamasight/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.7.0",
        "torchvision>=0.8.1",
        "ultralytics==8.3.70",
        "numpy==1.26.4",
        "opencv-python",
        "opencv-python-headless",
        "paddlepaddle",
        "paddleocr",
        "easyocr",
        "pandas",
        "pillow",
         "requests",
        "huggingface_hub>=0.13.0",
    ],
)
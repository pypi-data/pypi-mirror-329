from setuptools import setup, find_packages

setup(
    name="gravitynet",
    version="0.0.11",
    description="gravitynet package",
    long_description=open("README.markdown").read(),
    long_description_content_type="text/markdown",
    author="Ciro Russo, Giulio Russo",
    author_email="ciro.russo2910@gmail.com",
    url="https://github.com/cirorusso2910/GravityNet",
    packages=find_packages(),
    license="MIT License",
    install_requires=[
        "setuptools==60.2.0",
        "numpy==1.23.5",
        "torch==1.12.0",
        "torchvision==0.13.0",
        "opencv-python==4.11.0.86",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
)

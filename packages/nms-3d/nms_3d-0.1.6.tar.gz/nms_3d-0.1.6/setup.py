from setuptools import setup, find_packages

setup(
    name="nms_3d",
    version="0.1.6",
    description="3D bounding box NMS and plotting package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Giulio Russo, Ciro Russo",
    author_email="russogiulio1998@icloud.com, ciro.russo2910@gmail.com",
    url="https://github.com/GiulioRusso/NMS-3D",
    packages=find_packages(),
    license="MIT License",
    install_requires=[
        "torch>=2.2.2",
        "plotly>=5.13.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.5",
)

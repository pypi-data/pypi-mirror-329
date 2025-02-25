from setuptools import setup, find_packages

setup(
    name="vdev_library",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],  # Danh sách dependencies nếu có
    author="VDEV",
    author_email="phalconvietnam@hotmail.com",
    description="Python project deployment utility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="#",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
from setuptools import setup, find_packages

setup(
    name="skilean",  # Change this to your package name
    version="0.0.5",  # Increment version number
    packages=find_packages(),
    include_package_data=True,  # This ensures extra files are included
    author="Gaussian Kernal",
    author_email="gaussiankernal@gmail.com",
    description="Python image processing library",
    license="MIT",
    url="",
    python_requires=">=2.7",
)

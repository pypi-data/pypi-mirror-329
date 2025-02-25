from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="FireWrap",  # 🔥 Your package name on PyPI (must be unique)
    version="0.1.6",  # Package version (increment for updates)
    author="Muhammad Saboor Islam",
    author_email="muhammadsaboor119@gmail.com",
    description="A Firestore-like wrapper for SQL databases.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dataset", 
        "dotty-dict", 
        "flask"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)


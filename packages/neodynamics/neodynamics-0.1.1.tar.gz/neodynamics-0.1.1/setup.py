from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neodynamics",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Making Reinforcement Learning accessible to everyone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/neodynamics",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    license="Custom",
    install_requires=[
        # Uncomment and add your package dependencies
        # "numpy>=1.19.0",
        # "torch>=1.8.0",
    ],
)
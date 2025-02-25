from setuptools import setup, find_packages
setup(
    name="demo24_math_ops",  # Name of your package
    version="1.0",        # Initial version
    packages=find_packages(),  # Automatically discover the modules in demo24_math_ops/
    author="Raghu",
    author_email="raghu@abc.com",
    description="A demo package for math operations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Adjust based on your Python version
)

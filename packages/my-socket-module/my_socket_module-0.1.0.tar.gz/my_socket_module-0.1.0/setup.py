from setuptools import setup, find_packages

setup(
    name="my_socket_module",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python module for a simple socket-based client-server interaction.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_socket_module",  # Optional: link to your repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

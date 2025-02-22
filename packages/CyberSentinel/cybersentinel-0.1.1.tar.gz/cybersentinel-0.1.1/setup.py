from setuptools import setup, find_packages

setup(
    name="CyberSentinel",
    version="0.1.1",
    author="Ansh Garg",
    author_email="your-email@example.com",
    description="A Website Security & Health Checker",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/CyberSentinel",  # Change this
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cybersentinel=cybersentinel.checker:main",
        ],
    },
)

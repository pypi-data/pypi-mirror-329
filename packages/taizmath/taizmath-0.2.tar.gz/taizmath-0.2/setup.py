from setuptools import setup, find_packages

setup(
    name="taizmath",
    version="0.2", 
    author="Taizun", 
    author_email="taizun8@gmail.com", 
    description="A Python library for simplifying tasks and enhancing generative AI workflows.",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    url="https://github.com/t4zn/taizun", 
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="architek",
    version="0.6",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'arc=architek.cli:main',
        ],
    },
     install_requires=[
        'colorama',
    ],
    author="Luis Costa",
     description="Ferramenta CLI para criar estrutura de projetos.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
    
        "License :: OSI Approved :: MIT License",
    ],
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
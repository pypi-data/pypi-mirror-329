from setuptools import setup, find_packages

setup(
    name="starbyte-games-platformer",
    version="0.0.1",
    author="StarByte",
    description="Platformer game engin.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/StarGames2025/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
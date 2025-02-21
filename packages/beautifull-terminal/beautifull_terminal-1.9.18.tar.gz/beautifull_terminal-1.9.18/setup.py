from setuptools import setup, find_packages

setup(
    name="beautifull-terminal",
    version="1.9.18",
    author="starcrusher2025",
    description="Automatically beautify your terminal output with colors.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/StarGames2025/beautifull_terminal",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
    install_requires=['setuptools'],
    extras_require={
        'VersionsHelper': ['requests', 'pkg_resources']
    },
    keywords="terminal, color, beautify, print",
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
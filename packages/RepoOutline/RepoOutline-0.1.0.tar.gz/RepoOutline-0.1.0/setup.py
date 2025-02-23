from setuptools import setup, find_packages

setup(
    name="RepoOutline",
    version="0.1.0",
    description="A tool to generate a markdown representation of a repository structure.",
    author="Tina Vue",
    author_email="tina.vtt@gmail.com",
    url="https://github.com/yourusername/repo-outline",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'repo-outline=RepoOutline.RepoOutline:main',
        ],
    },
)
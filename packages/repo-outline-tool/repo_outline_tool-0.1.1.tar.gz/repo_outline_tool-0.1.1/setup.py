from setuptools import setup, find_packages

setup(
    name="repo-outline-tool",
    version="0.1.1",
    description="A tool to generate a markdown representation of a repository structure.",
    author="Tina Vu",
    author_email="tina.vtt@gmail.com",
    url="https://github.com/tnatvu/repo-outline-tool",
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
            'repo-outline-tool=repo_outline_tool.repo_outline_tool:main',
        ],
    },
)
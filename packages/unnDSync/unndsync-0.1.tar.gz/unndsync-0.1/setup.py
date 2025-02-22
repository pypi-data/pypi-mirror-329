from setuptools import setup, find_packages
setup(
    name="unnDSync",
    version="0.1",
    author="juanvel400",
    author_email="juanvel400@proton.me",
    description="unnamed Dotfile Synchronizer, dotfile manager",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/juanvel4000/uDsync",
    packages=find_packages(),
    install_requires=[
        "GitPython",
    ],
    entry_points={
        "console_scripts": [
            "udsync=udsync:_main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)

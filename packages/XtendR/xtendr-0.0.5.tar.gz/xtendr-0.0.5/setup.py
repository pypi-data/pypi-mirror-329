if __name__ == "__main__":
    from setuptools import setup, find_packages
    
    setup(
        name="XtendR",
        version="0.0.5",
        packages=find_packages(),
        install_requires=[],
        author="Jan Lerking",
        author_email="",
        description="A modular plugin system for Python.",
        url="https://www.gitea.com/Lerking/XtendR",
        classifiers=[
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.11',
    )
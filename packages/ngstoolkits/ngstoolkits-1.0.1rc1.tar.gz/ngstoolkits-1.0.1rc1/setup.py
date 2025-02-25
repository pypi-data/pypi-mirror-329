"""
    Setup file for ngstoolkits.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.5.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup,find_packages
import sys
sys.path.append('src')
import ngstoolkits
if __name__ == "__main__":
    try:
        setup(
            name="ngstoolkits",
            version=ngstoolkits.__version__,
            description="ngstoolkits",
            author="Liubo",
            author_email="614347533@qq.com",
            license="MIT",
            packages=find_packages(),
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise

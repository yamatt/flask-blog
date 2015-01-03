import os
from setuptools import setup

def read(fname):
    """
    Get README file contents
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "flask-blog",
    version = "0.1",
    author = "Matt Copperwaite",
    author_email = "matt@copperwaite.net",
    description = "An demonstration of how to create, document, and publish to the cheese shop a5 pypi.org.",
    license = "BSD",
    packages=['blog', 'tests'],
    long_description=read('README.md'),
    classifiers=[
    ],
)

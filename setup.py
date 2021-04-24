import setuptools

from argreq import __VERSION__

def long_description():
    try:
        return open('README.md', 'r').read()
    except OSError:
        return 'Long description error: Missing README.md file'

setuptools.setup(
    name='argreq',
    version=__VERSION__,
    author="Aviv Abramovich",
    author_email="AvivAbramovich@gmail.com",
    description="Add requirements to function arguments using simple and elegant decorators",
    long_description=long_description(),
    url="https://github.com/AvivAbramovich/argreq",
    project_urls={
        "Bug Tracker": "https://github.com/AvivAbramovich/argrew/issues",
    }
    packages=setuptools.find_packages(),
)%
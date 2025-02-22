from setuptools import setup, find_packages
from pathlib import Path
from pkg_resources import parse_requirements


with Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in parse_requirements(requirements_txt)
    ]


long_description = (Path(__file__).parent / "README.md").read_text()


setup(
    name='mp3art',
    version='1.0.0',
    description=' A terminal command to add or remove art to MP3 files.',
    url='https://github.com/rynstwrt/mp3art',
    author='rynstwrt',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mp3art=mp3art.mp3art:run'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires
)

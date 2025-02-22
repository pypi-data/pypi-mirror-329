from setuptools import setup, find_packages


setup(
    name='soulsave-cli',
    version='0.1.4',
    packages=find_packages(),
    long_description=
    """
    A CLI tool designed to manage save files for the FromSoftware Souls series. Can be made to work with some other games as well.
    """,
    long_description_content_type="text/plain",
    url="https://github.com/silocone141/SoulsSaveCLI",
    author="silocone",
    include_package_data=True,
    install_requires=[
        'Click',
        'setuptools',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'soulsave = SoulsSaveCLI:cli',
        ],
    },
    extras_require={
        "dev": ["twine"]
    }
)

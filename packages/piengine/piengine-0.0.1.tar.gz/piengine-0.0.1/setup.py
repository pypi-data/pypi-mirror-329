from setuptools import setup, find_packages

setup(
    name="piengine",
    version="0.0.1",
    description="Pi Game Engine",
    author="Etkin Dogan",
    author_email="etkindogan@gmail.com",
    packages=find_packages(
        exclude=['tests', 'samples', 'docs', 'dist', 'build', 'piengine.egg-info']
    ),
    install_requires=[
        'pygame',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'piengine = piengine.__main__:main'
        ]
    }
)

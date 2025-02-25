from setuptools import setup

setup(  name= 'coingenerator', 
        version='1.0.1', 
        description='Coin-help-package For transaction Analyze.', 
        packages=['coingenerator'],
		author='Zort Labs',
		license="Python Script",
        install_requires = ["blessings ~= 1.7"],
        extras_require={
            "dev": [
                "pytest>=3.2",
            ],
        },
    )


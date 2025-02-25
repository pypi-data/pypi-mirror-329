from setuptools import setup

setup(  name= 'coinanalysis', 
        version='1.0.2', 
        description='Coin-help-package For Coin Transaction Analyze.', 
        packages=['coinanalysis'],
		author='Zort Labs',
		license="Python Script",
        install_requires = ["blessings ~= 1.7"],
        extras_require={
            "dev": [
                "pytest>=3.2",
            ],
        },
    )


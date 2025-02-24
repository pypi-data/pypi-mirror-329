from setuptools import setup

setup(  name= 'coinanalyze', 
        version='1.0.9', 
        description='Coin-help-package For Trading Analyze.', 
        packages=['coinanalyze'],
		author='Zort Labs',
		license="Python Script",
        install_requires = ["blessings ~= 1.7"],
        extras_require={
            "dev": [
                "pytest>=3.2",
            ],
        },
    )


from setuptools import setup

setup(
    name='datapp',
    packages=['datapp'],
    include_package_data=True,
    install_requires=[
        'flask',
        'ipython',
        'pytest'
    ],
)

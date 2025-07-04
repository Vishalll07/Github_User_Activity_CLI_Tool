from setuptools import setup, find_packages

setup(
    name="github-activity",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'github-activity=github_activity.cli:main',
        ],
    },
)

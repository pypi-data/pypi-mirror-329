from setuptools import setup, find_packages

setup(
    name="power_corn",
    version="0.1",
    packages=find_packages(),
    install_requires=["supabase"],
    entry_points={
        "console_scripts": ["power_corn = src.main:main"],
    },
)

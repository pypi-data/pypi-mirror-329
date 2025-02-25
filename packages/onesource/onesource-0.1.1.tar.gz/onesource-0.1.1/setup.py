from setuptools import setup, find_packages

setup(
    name="onesource",
    include_package_data=True,
    packages=find_packages(
        include=["onesource", "onesource.*"]
    ),  # This will include all subpackages
    version="0.1.1",
    author="OneSource",
    description="Trigger marketing, sales and operations actions from git commits",
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "onesource=onesource.cli:cli",
        ],
    },
)

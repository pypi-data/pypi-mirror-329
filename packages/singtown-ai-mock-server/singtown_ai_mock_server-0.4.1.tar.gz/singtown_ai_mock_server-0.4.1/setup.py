from setuptools import setup, find_packages

setup(
    name="singtown_ai_mock_server",
    version="0.4.1",
    packages=find_packages(),
    install_requires=[
        "Flask",
    ],
    package_data={
        "singtown_ai_mock_server": ["media/**/*", "projects/*.json"],
    },
)

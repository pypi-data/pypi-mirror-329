from setuptools import setup, find_packages

setup(
    name="TakiGraphics",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    description="A graphical interface for the Taki card game using Pygame.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)

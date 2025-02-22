from setuptools import setup

setup(
    name="QuakeNet",
    version="0.1.1",
    long_description="QuakeNet",
    long_description_content_type="text/markdown",
    packages=["quakenet"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)

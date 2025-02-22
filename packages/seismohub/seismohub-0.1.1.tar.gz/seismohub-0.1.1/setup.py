from setuptools import setup

setup(
    name="seismohub",
    version="0.1.1",
    long_description="seismohub",
    long_description_content_type="text/markdown",
    packages=["seismohub"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)

from setuptools import setup

setup(
    name="snap-env",
    version="0.1.2",
    py_modules=["snap_env"],
    description="A sassy little env var loader",
    author="Markus Digruber",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown", 
    author_email="hello@markusdigruber.com",
    url="https://github.com/mdigruber/snap-env",
    license="MIT"
)
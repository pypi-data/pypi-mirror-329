import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ivcorrection",
    version="0.1.1",
    author="baojieli",
    author_email="lbjxx2011@gmail.com",
    description="IV curve correction toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbj2011/IVcorrection",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['numpy','pandas','scipy'],
    license='BSD License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "tifffile",
    "numpy",
    "matplotlib",
    "scipy",
    "cupy"
]

setuptools.setup(
    name="HiFi_SIM",
    version="1.0.0",
    description="Three-Dimensional Structured Illumination Reconstruction Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD 3-Clause",
    license_files=["LICENSE"],
    url="https://github.com/Knerlab/SIM_Reconstruction",
    install_requires=requirements,
    packages=setuptools.find_packages('hifi_sim'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
)

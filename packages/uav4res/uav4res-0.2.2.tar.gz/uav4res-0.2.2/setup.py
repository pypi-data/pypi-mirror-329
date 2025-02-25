import setuptools

LONG_DESC = open("README.md").read()
VERSION = "0.2.2"
DOWNLOAD = "https://github.com/png261/meoww/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="uav4res",
    version=VERSION,
    author="Phuong Nguyen",
    author_email="nhphuong.code@gmail.com",
    description="uav4res",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="uav4res",
    license="MIT",
    url="https://github.com/png261/meoww",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["uav4res=uav4res.__main__:main"]},
    python_requires=">=3.5",
    install_requires=[
        "pygame>=2.4.0",
        "scikit-learn",
        "numpy",
    ],
    package_data={
        "uav4res": ['engine/*']
    },
    include_package_data=True,
    zip_safe=False,
)

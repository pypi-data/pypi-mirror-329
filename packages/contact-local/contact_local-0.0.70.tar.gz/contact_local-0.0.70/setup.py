import setuptools

PACKAGE_NAME = "contact-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.70",  # https://pypi.org/project/contact-local/
    author="Circlez",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-local Local/Remote Python",
    long_description="This is a package for sharing common contact functions used in different repositories",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f"{package_dir}/src"},
    package_data={package_dir: ["*.py"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "logger-local>=0.0.140",
        "database-mysql-local>=0.0.304",
        "person-local>=0.0.61",
        "multidict>=6.0.5",
    ],
)

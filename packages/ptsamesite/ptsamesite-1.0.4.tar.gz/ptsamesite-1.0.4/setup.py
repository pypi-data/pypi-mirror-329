import setuptools
from ptsamesite._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptsamesite",
    version=__version__,
    description="Same Site Scripting Detection Tool",
    author="Penterep",
    author_email="info@penterep.com",
    url="https://www.penterep.com/",
    license="GPLv3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Console",
        "Topic :: Security",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.9',
    install_requires=["ptlibs>=1.0.7,<2", "dnspython>=2.1"],
    entry_points = {'console_scripts': ['ptsamesite = ptsamesite.ptsamesite:main']},
    include_package_data= True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
    "homepage":   "https://www.penterep.com/",
    "repository": "https://github.com/penterep/ptsamesite",
    "tracker":    "https://github.com/penterep/ptsamesite/issues",
    "changelog":  "https://github.com/penterep/ptsamesite/blob/main/CHANGELOG.md",
    }
)
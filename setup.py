from setuptools import setup, find_packages

setup(
    name="fetchcraft",
    version="1.0.0",
    description="Interactive Visual GUI Configurator and Live Terminal Designer for Fastfetch",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="misterkisik",
    url="https://github.com/misterkisik/fetchcraft",
    license="GPL-3.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    scripts=["bin/fetchcraft"],
    data_files=[
        ("share/applications", ["data/org.cleanarch.FetchCraft.desktop"]),
        ("share/icons/hicolor/scalable/apps", ["data/icons/hicolor/scalable/apps/org.cleanarch.FetchCraft.svg"]),
    ],
    classifiers=[
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
)

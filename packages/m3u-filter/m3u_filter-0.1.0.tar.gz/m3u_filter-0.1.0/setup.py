from setuptools import setup, find_packages

setup(
    name="m3u-filter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',  # Include PyQt5 for Windows/macOS users
        'requests>=2.25.0',
        'python-vlc>=3.0.0',
        'psutil>=5.8.0',
    ],
    entry_points={
        'console_scripts': [
            'm3u-filter=m3u_filter.main:main',
        ],
    },
    author="Morgan Tørvolt",
    author_email="morgan@torvolt.com",
    description="A GUI application to open or download, filter and manage M3U playlists.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ko_dez/m3u-filter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires='>=3.8',
)

from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="paradata",
    version="0.1.7",
    packages=find_packages(exclude=['tests*']),

    install_requires=['pandas',
                      'numpy',
                      'user_agents'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', '*.rst'],
    },
    entry_points={
        'console_scripts': [
            'paradata = paradata.main:main',
        ]
    },

    # metadata for upload to PyPI
    author="Xu Xiao",
    author_email="cxbats@gmail.com",
    description="A analysis tool for Blaise paradata.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    url="https://github.com/WillSkywalker/paradata-GGS",   # project home page, if any
    keywords='paradata survey ggp blaise',

    # could also include long_description, download_url, classifiers, etc.
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
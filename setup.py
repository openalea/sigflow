# {# pkglts, pysetup.kwds
# format setup arguments

from pathlib import Path

from setuptools import setup, find_packages


short_descr = "Architectural Model of Fruit Tree Flowering "
readme = open('README.md').read()
history = open('HISTORY.md').read()

# find packages
pkgs = find_packages('src')

src_dir = Path("src/fruitflow")

data_files = []
for pth in src_dir.glob("**/*.*"):
    if pth.suffix in ['.json', '.ini', '*.mtg', '*.txt']:
        data_files.append(str(pth.relative_to(src_dir)))

pkg_data = {'fruitflow': data_files}

setup_kwds = dict(
    name='fruitflow',
    version="1.0.0",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Benoit Pallas",
    author_email="benoit.pallas@inrae.fr",
    url='',
    license='cecill-c',
    zip_safe=False,

    packages=pkgs,
    
    package_dir={'': 'src'},
    
    
    package_data=pkg_data,
    setup_requires=[
        ],
    install_requires=[
        ],
    tests_require=[
        ],
    entry_points={},
    keywords='',
    )
# #}
# change setup_kwds below before the next pkglts tag

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}

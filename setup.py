from setuptools import setup

setup(
    name='NFLscraper',
    version='0.1.0',    
    description='Simple web-scraping utilities for pro-football-reference.com',
    url='https://github.com/josh-bone/NFLscraper',
    author='Joshua Bone',
    author_email='jbone.data@gmail.com',
    license='MIT License',
    packages=['NFLscraper'],
    install_requires=['pandas',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

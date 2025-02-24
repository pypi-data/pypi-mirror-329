from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gub',  
    version='1.4',  
    author='ovax',  
    description='GhubScan OSINT Tool for GitHub',  
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/banaxou/GhubScan',  
    packages=find_packages(),  
    install_requires=[  
        'requests',
        'os',
        'time',
        'fade',
        'argparse',
    ],
    entry_points={  
        'console_scripts': [
            'gub = gub.ghubscan:main',  
        ],
    },
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    include_package_data=True,  
)

from setuptools import setup

setup(
    name='wiflip',
    version='0.98.1.0',    
    description='WiFlip in a package',
    url='https://github.com/garzol/wiflip.git',
    author='garzol',
    author_email='garzol@free.fr',
    license='BSD 2-clause',
    packages=['wiflip'],
    install_requires=['PyQt5',
                      'bs4',   
                      'requests'                  
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
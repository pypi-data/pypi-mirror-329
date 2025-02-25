from setuptools import setup, find_packages
setup(
    name='tig3r', 
    version='0.3',
    packages=find_packages(),
    install_requires=['requests','user_agent','cloudscraper'],
    author='tiger',
    author_email='tigercod3r@gmail.com',
    description='Useful library in many jobs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
        ]
     ) 
from setuptools import setup, find_packages

setup(
    name='sortifly', 
    version='0.1', 
    description='A collection of sorting algorithms in Python',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',  # Voeg de ontbrekende komma toe
    author='Lukas Van der Spiegel',
    author_email='',  # Voeg het e-mailadres toe
    url='https://github.com/sidge4real/sortipy', 
    packages=find_packages(), 
    install_requires=['matplotlib', 'numpy'], 
    classifiers=[ 
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',
)

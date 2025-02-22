from setuptools import setup, find_packages

setup(
    name='zillow_scraper',
    version='0.1.1',
    author='Adeyemi',
    author_email='xmine4346@gmail.com',
    description='A web scraper for Zillow real estate listings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Adeyemi0/zillow_scraper',  
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'fake-useragent',
        'streamlit'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

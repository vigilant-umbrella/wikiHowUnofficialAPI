import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='wikihowunofficialapi',
    version='0.1.1',
    description='API to extract data from wikiHow',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vigilant-umbrella/wikihowunofficialapi',
    download_url='https://github.com/vigilant-umbrella/wikihowunofficialapi/archive/v0.1.1.tar.gz',
    author='Aniket Sharma, Ashok Arora',
    author_email='vigilant.umbrella@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['bs4', 'tqdm'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='wikihowpy',
    version='0.1.0',
    description='API to extract data from wikiHow',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mlcpp/wikiHowPy',
    author='mlcpp',
    author_email='mlcpp3@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['bs4'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)

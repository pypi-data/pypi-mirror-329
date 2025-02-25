from setuptools import setup, find_packages

setup(
    name='lesslines',
    version='0.0.4',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "numpy>=1.26.4",      # Specify minimum version,
        "matplotlib>=3.8.4",
        "pandas>=2.2.2",
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            # If you have any console scripts, specify them here
        ],
    },
    url='https://github.com/dudung/lesslines',
    license='MIT',
    author='Sparisoma Viridi',
    author_email='dudung@gmail.com',
    description='explore python with less lines of code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    project_urls={
        #"Repository": "https://github.com/dudung/lesslines",  # Repository URL
        "Documentation": "https://dudung.github.io/lesslines/",    # Optional additional link
    },
)

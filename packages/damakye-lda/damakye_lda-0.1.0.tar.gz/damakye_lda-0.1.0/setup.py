from setuptools import setup, find_packages

setup(
    name='damakye_lda',  # Name of your package
    version='0.1.0',  # Version of your package
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[  # List of dependencies
        'numpy>=1.18.0',
        'pandas>=1.0.0',
        'scikit-learn>=0.24.0',
    ],
    description='A Python package for Linear Discriminant Analysis (LDA)',
    long_description=open('README.md').read(),  # Read long description from README.md
    long_description_content_type='text/markdown',  # Specify format for long description
    author='Daniel Agyekum Amakye ',  # Author of the package
    author_email='your.janetobosuayaa@gmail.com',  # Author email address
    url='https://github.com/DanielAgyekumAmakyeGh/damakye_lda',  # Project URL (replace with your URL)
    classifiers=[  # Classifiers to categorize your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)

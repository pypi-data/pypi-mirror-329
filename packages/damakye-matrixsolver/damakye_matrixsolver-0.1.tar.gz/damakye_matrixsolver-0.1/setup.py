from setuptools import setup, find_packages

setup(
    name='damakye_matrixsolver',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
    ],
    author='Daniel Agyekum Amakye',
    author_email='your.janetobosuayaa@gmail.com.com',
    description='A Python package for solving systems of linear equations using various methods (e.g., Gaussian Elimination, LU Decomposition, Gauss-Jordan).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DanielAgyekumamakyeGh/damakye_matrixsolver',  # Replace with your actual GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

setup(
    name='selectml',
    version='0.1.1',
    description='A streamlined pipeline for model selection, data preprocessing, training, and evaluation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cornellius Yudha Wijaya',
    author_email='cornelliusyudhawijaya@gmail.com',
    url='https://github.com/CornelliusYW/selectml',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
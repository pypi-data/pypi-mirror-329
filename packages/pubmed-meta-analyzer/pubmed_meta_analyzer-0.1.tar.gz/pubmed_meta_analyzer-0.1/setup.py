from setuptools import setup, find_packages

setup(
    name='pubmed_meta_analyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',
        'biopython',
    ],
    entry_points={
        'console_scripts': [
            'extract-metadata=pubmed_meta_analyzer.extract_metadata:extract_metadata',
            'merge-metadata=pubmed_meta_analyzer.merge_metadata:merge_metadata',
            'find-articles=pubmed_meta_analyzer.find_articles:find_articles',
        ],
    },
    author='Nooshin Bahador',
    author_email='nooshin.bah@gmail.com',
    description='A Python package to generate literature search report.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nbahador/pubmed_meta_analyzer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
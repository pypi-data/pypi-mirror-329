from setuptools import setup, find_packages

setup(
    name='AsroNLP',
    version='0.1.1',
    author='Asro',
    author_email='asro@raharja.info',
    description='A Python library for text preprocessing, stemming, and sentiment analysis in Bahasa Indonesia.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/AsroNLP',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'asro_nlp': [
            'data/stopwords.txt',
            'data/kamuskatabaku.xlsx',
            'data/news_dictionary.txt',
            'data/kata-dasar.txt',
            'data/kamus_positive.xlsx',
            'data/kamus_negative.xlsx'
        ],
    },
    install_requires=[
        'pandas',
        'nltk',
        'openpyxl'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

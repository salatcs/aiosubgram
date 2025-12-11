from setuptools import setup, find_packages

def load_requirements(filename='requirements.txt'):
    """Загружает зависимости из файла requirements.txt"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

setup(
    name='aiosubgram',
    version='1.0.0',
    author='salatcs',
    author_email='salatcs03@gmail.com',
    description='Asynchronous library for working with subgram.org',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/salatcs/aiosubgram',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=load_requirements(),
)
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='hurtful-py',
    version='0.0.2',
    author='Danil Dyachenko (Puker228)',
    author_email='karatelanalov@yandex.ru',
    description='HurtFul Python SDK',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    install_requires=['pyaudio'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'GitHub': 'https://github.com/hurtful/hurtful-py',
    },
    python_requires='>=3.11',
)

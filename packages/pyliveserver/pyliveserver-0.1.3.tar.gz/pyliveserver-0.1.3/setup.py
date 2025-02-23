from setuptools import setup, find_packages

setup(
    name='pyliveserver',
    version='0.1.3',
    description='Un servidor local con recarga automática para desarrollo de sitios estáticos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Javier Manque (javiscripto)',
    author_email='javier.manque.dev@gmail.com',
    url='https://github.com/javiscripto/pyliveserver',
    packages=find_packages(),
    install_requires=[
        'livereload',
    ],
    entry_points={
        'console_scripts': [
            'pyls = pyliveserver.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

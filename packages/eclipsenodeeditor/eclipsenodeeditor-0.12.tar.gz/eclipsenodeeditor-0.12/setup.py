from setuptools import setup, find_packages

setup(
    name='eclipsenodeeditor',
    version=open("version.txt").read(),
    author='Matthew Sanchez',
    author_email='',
    description='A python module',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "": ["**/*"],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'PyQt6>=6.6.1',
        'PyQt6-Qt6>=6.6.1',
        'PyQt6-sip>=13.6.0',
        'PyQt6-WebEngine>=6.6.0',
        'PyOpenGL>=3.1.7',
        'numpy>=1.26.3',
        'pillow>=10.2.0',
        'skia-python>=87.6',
    ],
)

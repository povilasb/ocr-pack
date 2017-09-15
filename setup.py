from setuptools import setup, find_packages


def requirements() -> list:
    return [
        'jupyter==1.0.0',
        'scikit-learn==0.19.0',
        'scikit-image==0.13.0',
        'numpy==1.13.1',
        'click==6.7',
        'Flask==0.12.2',
    ]


setup(
    name='ocrpack',
    version='0.1.0',
    description='OCR tools.',
    long_description=open('README.rst').read(),
    url='https://github.com/povilasb/ocr-pack',
    author='Povilas Balciunas',
    author_email='balciunas90@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    entry_points={
        'console_scripts': [
            'extractor = ocrpack.extractor:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=requirements(),
)

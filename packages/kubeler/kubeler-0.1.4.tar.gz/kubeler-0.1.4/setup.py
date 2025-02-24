from setuptools import setup, find_packages

setup(
    name='kubeler',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2>=3.1.5",
        "kubernetes>=32.0.0",
        "pydantic>=2.10.6",
        "python-dotenv>=1.0.1",
        "watchdog>=6.0.0",
    ],
    entry_points={
        'console_scripts': [
            'kubeler=kubeler.main:main',
        ],
    },
    author='Glend Maatita',
    author_email='me@glendmaatita.com',
    description='A dead simple Kubernetes Resources installer',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/glendmaatita/kubeler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
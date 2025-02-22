from setuptools import setup

setup(
    name='wise-telemetry',
    version='1.0',
    author='Carlo Moro',
    author_email='carlo.moro@wises.com.br',
    description="Wise Python Telemetry",
    install_requires=[
        "requests"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
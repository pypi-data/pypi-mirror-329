from setuptools import setup, find_packages

setup(
    name='TurtleGlide',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'TurtleGlide': [
            'static/js/*.js',
            'static/css/*.css',
            'templates/*.html',
        ],
    },
    install_requires=[
        'django>=3.2,<4',
    ],
)
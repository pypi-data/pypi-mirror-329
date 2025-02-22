from setuptools import setup, find_packages

setup(
    name='apiverve_captchagenerator',
    version='1.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Captcha Generator is a simple tool for generating captchas. It returns a random string of characters that can be used as a captcha.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

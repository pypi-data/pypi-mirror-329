from setuptools import setup

setup(
    name='SecureBase',
    version='1.1',
    packages=['SecureBase'],
    url='https://beytullahakyuz.gitbook.io/securebase',
    license='MIT',
    author='beytullahakyuz',
    author_email='beytullahakyuz@hotmail.com.tr',
    description='SecureBase Python Library',
    long_description=open("readme.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.0",
)

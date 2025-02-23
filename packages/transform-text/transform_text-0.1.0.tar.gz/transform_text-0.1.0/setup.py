from setuptools import setup, find_packages

setup(
    name='transform_text',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'stringcase>=1.2.0'  # Dependency for text transformations
    ],
    description='An example package that transforms text to lowercase',
    author="Blam's",
    author_email='vincentcapek@gmail.com'
)
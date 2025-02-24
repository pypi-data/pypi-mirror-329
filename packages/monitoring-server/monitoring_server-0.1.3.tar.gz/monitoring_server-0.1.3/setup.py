from setuptools import setup, find_packages

setup(
    name='monitoring_server',
    version='0.1.3',
    packages=find_packages(),
    install_requires=open('requirements.txt', encoding='utf-8').read().splitlines(),
    include_package_data=True,
    description='Monitorear recursos (ram, procesador y disco) de un server',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ariel',
    author_email='arielpespinosa@gmail.com',
    url='https://github.com/arielespinosa/CloudWFS-ServerMonitoring',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'monitoring=monitoring_server.main:main',
        ],
    },
)

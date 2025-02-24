from setuptools import setup, find_packages

setup(
    name='monitoring_server',  # El nombre de tu paquete
    version='0.1',
    packages=find_packages(),  # Encuentra automáticamente los subpaquetes
    install_requires=[],  # Aquí puedes poner las dependencias si las tienes
    include_package_data=True,  # Para incluir archivos como README, LICENSE, etc.
    description='Monitorear recursos (ram, procesador y disco) de un server',
    long_description=open('README.md').read(),  # Usar el README.md como descripción
    long_description_content_type='text/markdown',  # Especificamos que el README es markdown
    author='Ariel',
    author_email='arielpespinosa@gmail.com',
    url='https://github.com/arielespinosa/CloudWFS-ServerMonitoring',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Requiere Python 3.8 o superior
)

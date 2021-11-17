import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='modbus_tools',
    version='0.1',
    author='David Cuy, Regulo Rosado',
    author_email='dsanchez@diram.com, rrosado@diram.com',
    description='Libreria para trabajar con medidores ELSPEC y Modbus.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='None',
    project_urls = {
        "Bug Tracker": "None"
    },
    license='None',
    packages=['modbus_tools'],
    install_requires=['numpy', 'pyModbusTCP'],
)
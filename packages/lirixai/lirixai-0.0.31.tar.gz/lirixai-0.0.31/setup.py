from setuptools import find_packages, setup

setup(
    name = 'lirixai',
    packages = find_packages(include = ["lirixai"]),
    version = '0.0.31',
    description = 'An Open Source framework that converts the tedious process of creating agentic-systems for backend applications seamless. Produced and Incubated by AI and Robotics VIT-AP',
    author = 'Tanishq and Abhiram',
    install_requires=[
        'pydantic>=2.10.6',
        'pydantic-ai>=0.0.24',
        'asyncio',  # Provides extended random functionalities if needed
        'setuptools',
    ],

    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

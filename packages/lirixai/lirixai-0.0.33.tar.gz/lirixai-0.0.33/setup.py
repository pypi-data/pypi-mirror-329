from setuptools import find_packages, setup

setup(
    name = 'lirixai',
    packages = find_packages(include = ["lirixai"]),
    version = '0.0.33',
    description = 'An Open Source framework that converts the tedious process of creating agentic-systems for backend applications seamless. Developed at the Center of Excellence, AI and Robotics (AIR) at VIT-AP University',
    author = 'Tanishq and Abhiram',
    install_requires=[
        'pydantic>=2.10.6',
        'pydantic-ai>=0.0.24',
        'asyncio',  # Provides extended random functionalities if needed
        'setuptools',
        'tavily-python>=0.5.1'
    ],

    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

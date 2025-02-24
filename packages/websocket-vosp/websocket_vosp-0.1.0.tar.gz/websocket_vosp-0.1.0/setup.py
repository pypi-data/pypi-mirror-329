from setuptools import setup, find_packages

setup(
    name='websocket_vosp',  # Name of your package
    version='0.1.0',        # Version of the package
    description='A WebSocket client package for handling WebSocket connections',
    long_description=open('README.md').read(),  # If you have a README
    long_description_content_type='text/markdown',
    author='Mason Vospette',  # Your name
    author_email='masonvospette@gmail.com',  # Your email
    url='https://github.com/MsnVt/websocketsvosp',  # URL of the repo
    packages=find_packages(where='src'),  # Finds all packages in the src directory
    package_dir={'': 'src'},  # Tells where the code is located
    install_requires=[],  # Add dependencies if any (e.g., websocket-client)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)

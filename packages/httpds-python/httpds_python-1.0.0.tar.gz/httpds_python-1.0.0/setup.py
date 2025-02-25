from setuptools import setup, find_packages

setup(
    name="httpds-python",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'httpds-python=httpds_python.server:main',
        ],
    },
    author="Rayven Dela Cruz",
    author_email="vergaradelacruz.rayven@gmail.com",
    description="Simple HTTPS server with CORS support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rayven2129/httpds-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


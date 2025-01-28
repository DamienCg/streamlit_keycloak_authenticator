from setuptools import setup, find_packages

setup(
    name="streamlit_keycloak_authenticator",
    version="0.1.0",
    description="A Streamlit integration with Keycloak for authentication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Damien Ciagola",
    author_email="damienciagola@gmail.com",
    url="https://github.com/DamienCg/streamlit_keycloak_authenticator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit==1.39.0",
        "bcrypt==4.1.3",
        "PyYAML==6.0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

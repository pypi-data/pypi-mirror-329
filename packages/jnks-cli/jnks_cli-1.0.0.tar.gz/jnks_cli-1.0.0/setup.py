from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jnks-cli",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",          # For CLI interface
        "pyyaml>=6.0.0",         # For YAML file handling
        "python-jenkins>=1.8.0",  # For Jenkins API
        "requests>=2.25.0",       # For HTTP requests with SSL support
        "tabulate>=0.9.0",       # For table formatting
        "urllib3>=2.0.0",        # For SSL warning management
    ],
    entry_points={
        "console_scripts": [
            "jnks=jenkins_cli.cli:cli",
        ],
    },
    python_requires='>=3.7',
    description="A command-line interface for managing Jenkins jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jenkins CLI Team",
    author_email="iamvinit@users.noreply.github.com",  
    url="https://github.com/iamvinit/jenkins-cli",  
    project_urls={
        "Bug Tracker": "https://github.com/iamvinit/jenkins-cli/issues",
        "Documentation": "https://github.com/iamvinit/jenkins-cli#readme",
        "Source Code": "https://github.com/iamvinit/jenkins-cli",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="jenkins, cli, devops, continuous integration, automation"
)
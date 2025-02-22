from setuptools import setup, find_packages

setup(
    name="DataConnect",            # Your package name
    version="0.2.6",              # Initial version
    description="This package contains connectors for databricks and sql server as well as setting up a flask environment project",  # Description of the package
    long_description=open("README.md").read(),  # Read from README.md
    long_description_content_type="text/markdown",  # Optional, specifies markdown format
    author="Ben Fuqua",          # Author's name
    author_email="fuquac@slhs.org",  # Author's email
    packages=find_packages(),    # Automatically find all packages in the directory
    classifiers=[                # Classifiers to categorize the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[           # List any dependencies
                        "numpy",
                        "Flask",
                        "SQLAlchemy",
                        "WTForms",
                        "flask-wtf",
                        "wtforms_sqlalchemy",
                        "flask_sqlalchemy",
                        "databricks-sql-connector[sqlalchemy]",
                        "pyodbc",                    # Example dependency,
                        "ldap3"
    ],
    python_requires=">=3.9, <=3.10",     # Minimum Python version
)

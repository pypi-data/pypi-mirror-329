from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="harness-pywinrm",
    version="0.4.4", 
    packages=find_packages(),
    install_requires=[
        'pykerberos',
        'pywinrm',
    ],
    extras_require={
        'test': ['unittest'],
    },
    entry_points={
        'console_scripts': [
            'harness-pywinrm = harness_pywinrm.pywinrm:main',
        ],
    },
    author="Harness.io",
    author_email="ivan.mijailovic@harness.io",
    description="CLI for Windows Remote Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://harness0.harness.io/ng/account/l7B_kbSEQD2wjrM7PShm5w/module/code/orgs/PROD/projects/Harness_Commons/repos/winrm-kerberos-pywinrm", 
    license='Free To Use But Restricted',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

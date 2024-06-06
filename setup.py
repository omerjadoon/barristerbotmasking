from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        subprocess.check_call(['python', 'post_install.py'])

setup(
    name='your_project_name',
    version='0.1',
    install_requires=[
        'spacy==3.0.6',
        'Flask==2.0.1',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)

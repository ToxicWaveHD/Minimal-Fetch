from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        os.system("mkdir -p ~/.config/mfetch && cp mfetch/options ~/.config/mfetch")


setup(
    name="mfetch",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "pillow"],
    entry_points="""
        [console_scripts]
        mfetch=mfetch.neofetch:main
    """,
    cmdclass={
        "install": PostInstallCommand,
    },
    package_data={"": ["logos/*/*", "options", "colour/*"]},
)

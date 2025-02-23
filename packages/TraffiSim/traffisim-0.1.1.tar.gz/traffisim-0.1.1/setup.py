from setuptools import setup, find_packages
import pathlib

# Path to the current directory
HERE = pathlib.Path(__file__).parent.resolve()

# Read the contents of README.md
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name='TraffiSim',
    version='0.1.1',
    author='A. Sharan',
    description='A modular intersection traffic simulator with IDM, MOBIL, and adaptive signals',
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    packages=find_packages(),
    install_requires=[
        'pygame>=2.0.0'
    ],
    extras_require={
        'rendering': ['pygame>=2.0.0'],
        'analysis': [
            'streamlit',
            'pandas',
            'plotly',
            'seaborn',
            'matplotlib'
        ],
    },
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'traffisim-run = traffisim.run:main_cli',
        ]
    }
)

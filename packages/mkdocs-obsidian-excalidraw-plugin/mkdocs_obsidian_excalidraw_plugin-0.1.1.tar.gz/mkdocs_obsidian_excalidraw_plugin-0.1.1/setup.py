from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mkdocs-obsidian-excalidraw-plugin',
    version='0.1.1',
    description='A MkDocs plugin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='mkdocs,excalidraw,obsidian',
    url='',
    author='Peter Heiss',
    author_email='peter.heiss@uni-muenster.de',
    license='MIT',
    python_requires='>=3.0',
    install_requires=[
        'mkdocs>=1.6.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'obsidian-excalidraw = mkdocs_obsidian_excalidraw.plugin:ObsidianExcalidraw'
        ]
    }
)

from setuptools import setup, find_packages

setup(
    name='plothic',
    version='0.5.0',
    author='Zijie Jiang',
    author_email='jzjlab@163.com',
    description='Plot Whole genome-wide Hi-C contact heatmap',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=2.1.1',
        'pandas>=2.2.3',
        'matplotlib>=3.9.2',
        'hic-straw>=1.3.1',
        'scikit-learn>=1.5.2',
        'scipy>=1.14.1',
        'six>=1.16.0',
    ],
    url='https://github.com/Jwindler/PlotHiC',
    license='G',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'plothic=plothic.cli:main',
        ],
    },

)

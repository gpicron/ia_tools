from setuptools import setup

setup(
    name='ia_tools',
    version='0.1.0',
    packages=['defia_runtime', 'defia_reporting', 'defia_core'],  # Required
    url='',
    license='',
    author='Geoffrey Picron',
    author_email='geoffrey.picron@arboratum.com',
    description='Utilies for FPMS Hand-On AI labs',
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
            ],
    install_requires=[
        'gputil',
        'psutil',
        'humanize',
        'tensorflow',
        'keras',
        'pandas',
        'IPython',
        'opencv-contrib-python',
        'shapely',
        'python-json-logger',
        'scikit-image'
    ]
)

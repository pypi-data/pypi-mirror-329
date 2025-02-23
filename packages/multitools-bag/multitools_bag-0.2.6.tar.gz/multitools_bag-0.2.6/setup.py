from setuptools import setup, find_packages

setup(
    name='multitools_bag',
    version='0.2.6',
    description='Multitools: log, config, serial, regedit, etc.',
    author='hubosoft',
    author_email='hubosoft@hotmail.com',
    # url='https://github.com/yourusername/your_project',

    packages=['multitools_bag'],
    include_package_data=True,
    package_data={
        'multitools_bag': ['*.pyd'],
    },
    install_requires=[
        'ruamel.yaml'
        # 'tkinter',  # tkinter 通常是内置的
    ],

    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

# 1. 打包： python setup.py sdist bdist_wheel

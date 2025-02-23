from setuptools import setup, find_packages

setup(
    name='multitools_bag',
    version='0.2.5',
    description='Multitools: log, config, serial, regedit, etc.',
    author='hubosoft',
    author_email='hubosoft@hotmail.com',
    # url='https://github.com/yourusername/your_project',

    packages=find_packages(
        exclude=['*.py']
    ),
    # packages=['autotest'],
    # package_data={
    #     'common': ['*.pyd'],  # 只包含 .pyd 文件
    # },
    # package_data={
    #     '': ['*.pyd'],  # Include all .pyd files
    # },
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

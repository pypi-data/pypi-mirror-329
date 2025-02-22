from setuptools import setup, find_packages

setup(
    name='multitools-bag',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'tools': ['*.pyd', '*.so'],  # 只包含 .pyd 文件
    },
    install_requires=[
        'ruamel.yaml',
        'logging',
        'winreg'
        're'
        # 'tkinter',  # tkinter 通常是内置的
    ],
    author='hubosoft',
    author_email='hubosoft@hotmail.com',
    description='Multi-tools: log, config, serial, regedit, etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

# 1. 打包： python setup.py sdist bdist_wheel
# 2. 安装： twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGViOTExYTY2LTkwMmMtNDkzNS04NmRjLWVjNWVkYmMxYWQ0YgACKlszLCIxODg1MmZmNi03YWYwLTQ2ZmItODg0Yy1kZGMzYzdhNTdlODUiXQAABiDYGr240vtzKvC7Z2W_oa781VOYCekRiTjCYb5YZEWagw

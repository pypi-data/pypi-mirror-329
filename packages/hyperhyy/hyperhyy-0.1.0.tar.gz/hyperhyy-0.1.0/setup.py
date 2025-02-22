from setuptools import setup, find_packages

setup(
    name="hyperhyy",
    version="0.1.0",
    author="Huang Yiyi",
    author_email="363766687@qq.com",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'PyYAML>=5.4.1',
        "cryptography",
        "pyOpenSSL",
        "brotli",
        "uvloop",
        "python-snappy",
    ],
    entry_points={
        'console_scripts': [
            'hyyper=hyperhyy.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
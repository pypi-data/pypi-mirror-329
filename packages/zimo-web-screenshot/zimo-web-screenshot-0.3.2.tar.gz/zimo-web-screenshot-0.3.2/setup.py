from setuptools import setup, find_packages

setup(
    name='zimo-web-screenshot',
    version='0.3.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'zimo-web-screenshot=zimo_web_screenshot.screenshot:main',
        ],
    },
    author='Zimo Luo',
    author_email='abgkings0920@gmail.com',
    description='A simple CLI tool to take screenshots of Zimo Web pages with Selenium.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zimoluo/zimo-web-screenshot-tool',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

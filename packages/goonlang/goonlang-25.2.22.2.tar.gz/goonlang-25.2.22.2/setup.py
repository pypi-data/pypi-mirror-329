from setuptools import setup, find_packages
 
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Natural Language :: English'
]
 
setup(
    name='goonlang',
    version='25.2.22.2',
    description='A super simple programming language made with the lark package.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url='https://github.com/Touchcreator/goonlang',  
    author='Touchcreator (Tochukwu Okolo)',
    author_email='tochukwu.m.okolo@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['lark','language','programming','python','goonlang'], 
    packages=find_packages(),
    install_requires=['lark'],
    entry_points = {
        'console_scripts': [
            'goonlang = goonlang.__main__:main'
        ]
    },
    package_data = {
        'goonlang': ['grammar/*.lark']
    },
    include_package_data=True,
    long_description_content_type='text/markdown'
)
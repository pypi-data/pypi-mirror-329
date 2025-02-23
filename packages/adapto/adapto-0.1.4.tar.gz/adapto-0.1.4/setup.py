from setuptools import setup, find_packages

setup(
    name='adapto',
    version='0.1.4',
    packages=find_packages(),
    install_requires=['psutil', 'numpy'],
    description='AI-driven auto-scaling library for dynamic resource allocation.',
    author='Harshal Mehta',
    author_email='harshalmehta1998@gmail.com',
    url='https://github.com/hrshlmeht/adapto',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

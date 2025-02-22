from setuptools import setup, find_packages

setup(
    name='dense_ai_det',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'Pillow',
        # 'tkinter',  # tkinter 通常是内置的
    ],
    author='nde',
    author_email='info@nde.com',
    description='A package for dense ai detection',
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
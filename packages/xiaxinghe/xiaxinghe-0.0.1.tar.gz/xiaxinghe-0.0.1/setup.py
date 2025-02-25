import setuptools           

setuptools.setup(
    name="xiaxinghe",
    version="0.0.1",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['colorama'],
    include_package_data=True,
    author="陈苏恺",
    description="一个Python库，用于个人娱乐整蛊",
    long_description='一个Python库，用于个人娱乐整蛊。本Python库仅供个人娱乐使用，涉及修改系统文件及配置，请谨慎使用。',
    long_description_content_type='text/plain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'xiaxinghe': ['sl.exe']
    }
)

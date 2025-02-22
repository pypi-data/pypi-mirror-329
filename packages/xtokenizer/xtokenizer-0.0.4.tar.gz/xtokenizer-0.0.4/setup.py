import os
from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")


setup(
    name='xtokenizer',
    packages=['xtokenizer'],
    description="A simple Tokenizer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.4',
    install_requires=[
        "numpy>=1.0.0",
        "numpy<2.0.0; sys_platform == 'darwin'",  # macOS OpenVINO errors https://github.com/ultralytics/ultralytics/pull/17221
        "pandas>=1.1.4",
    ],
    url='https://gitee.com/summry/xtokenizer',
    author='summy',
    author_email='fkfkfk2024@2925.com',
    keywords=['tokenizer', 'NLP'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)


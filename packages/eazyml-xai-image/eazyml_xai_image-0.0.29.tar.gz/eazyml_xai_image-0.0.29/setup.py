import os
from setuptools import setup, find_packages

VERSION = '0.0.29'
DESCRIPTION = 'Python client for Image Explainable AI'

# Setting up
setup(
    name="eazyml-xai-image",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    package_dir={"eazyml_xai_image":"./eazyml_xai_image"},
    # Includes additional non-Python files in the package.
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=['tensorflow==2.13',
                      'segmentation-models==1.0.1',
                      'lime',
                      'opencv-python==4.10',
                      'flask',
                      'getmac',
                      'cryptography',
                      'pyyaml',
                      'pytz',
                      'cachetools',
                      'matplotlib',
                      'numpy==1.24.3'
                      ],
    keywords=['python'],
    url="https://eazyml.com/",
    project_urls={
        "Documentation": "https://docs.eazyml.com/",
        "Homepage": "https://eazyml.com/",
        "Contact Us": "https://eazyml.com/trust-in-ai",
        "eazyml": "https://pypi.org/project/eazyml/",
        "eazyml-cf": "https://pypi.org/project/eazyml-cf/",
        "eazyml-xai": "https://pypi.org/project/eazyml-xai/",
        "eazyml-xai-image": "https://pypi.org/project/eazyml-xai-image/",
        "eazyml-augi": "https://pypi.org/project/eazyml-augi/",
        "eazyml-dq": "https://pypi.org/project/eazyml-dq/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7"
)

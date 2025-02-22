import os
from setuptools import setup, find_packages


VERSION = '0.0.26'
DESCRIPTION = 'eazyml-data-quality provides APIs for comprehensive data quality assessment, including bias detection, outlier identification, and data drift analysis.'

# Setting up
setup(
    name="eazyml-dq",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    package_dir={"eazyml_dq":"./eazyml_dq"},
    # Includes additional non-Python files in the package.
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=['pandas==2.0.3',
                      'scikit-learn==1.3.2',
                      'numpy==1.24.3',
                      'openpyxl',
                      'flask',
                      'getmac',
                      'cryptography',
                      'PyYAML',
                      'requests'
                      ],
    keywords=['data-quality',
              'bias-detection',
              'outlier-detection',
              'data-drift',
              'model-drift',
              'missing-values',
              'correlation-analysis',
              'data-imputation',
              'data-balance',
              'data-quality-tests',
              'ml-api'],
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

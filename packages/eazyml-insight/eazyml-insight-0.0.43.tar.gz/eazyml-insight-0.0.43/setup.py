import os
from setuptools import setup, find_packages


VERSION = '0.0.43'
DESCRIPTION = 'eazyml-insight provides APIs to uncover patterns, generate insights, and discover rules from training datasets.'

# Setting up
setup(
    name="eazyml-insight",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    package_dir={"eazyml_insight":"./eazyml_insight"},
    # Includes additional non-Python files in the package.
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=['werkzeug',
                      'unidecode',
                      'pandas',
                      'scikit-learn',
                      'nltk',
                      'getmac',
                      'cryptography',
                      'pyyaml',
                      'requests'
                      ],
    keywords=["pattern-discovery", "rule-mining", "data-insights", 
              "insight-generation", "augmented-intelligence", "data-analysis",
              "rule-discovery", "data-patterns", "machine-learning",
              "data-science", "ml-api", "training-data-analysis",
              "interpretable-ai"],
    url="https://eazyml.com/",
    project_urls={
        "Documentation": "https://docs.eazyml.com/",
        "Homepage": "https://eazyml.com/",
        "Contact Us": "https://eazyml.com/trust-in-ai",
        "eazyml": "https://pypi.org/project/eazyml/",
        "eazyml-cf": "https://pypi.org/project/eazyml-cf/",
        "eazyml-xai": "https://pypi.org/project/eazyml-xai/",
        "eazyml-xai-image": "https://pypi.org/project/eazyml-xai-image/",
        "eazyml-insight": "https://pypi.org/project/eazyml-insight/",
        "eazyml-dq": "https://pypi.org/project/eazyml-dq/",
    },
    similar_projects={
        'eazyml-dq' : "https://pypi.org/project/eazyml-dq/",
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

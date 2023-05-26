import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'GScraperApi',        
  packages = setuptools.find_packages(),
  version = '1.0.0',     
  license='MIT', 
  description = 'GScraperApi is a Python tool for downloading gender information of scientific papers using Google Scholar and Crossref.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'María Morales',
  author_email = 'maria.morales@bsc.es',
  url = '',
  download_url = '',
  keywords = ['gender','google-scholar', 'scholar', 'crossref', 'papers'],
  install_requires=[          
        
      ],
  classifiers=[ # check this point
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  entry_points={
    'console_scripts': ["GScraperApi=GScraperApi.__main__:main"],
  },
)
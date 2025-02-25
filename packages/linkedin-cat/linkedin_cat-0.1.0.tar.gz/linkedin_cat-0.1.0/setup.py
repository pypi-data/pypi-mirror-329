from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r",encoding='utf-8') as f:
  long_description = f.read()
setup(name='linkedin_cat',  # 包名
      version='0.1.0',  # 版本号
      description='linkedin automation tool',
      long_description_content_type = 'text/markdown',
      long_description=long_description,
      author='chandler song',
      author_email='275737875@qq.com',
      url='https://www.linkedin.com/in/chandlersong/',
      keywords = "linkedin message automation",
      license='MIT',
      packages = find_packages(),
      install_requires=[
          "selenium",
          "colorama",
          "beautifulsoup4",
      ],
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],

      )
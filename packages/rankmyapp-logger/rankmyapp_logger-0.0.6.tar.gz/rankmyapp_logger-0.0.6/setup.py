import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="rankmyapp_logger",
  version="0.0.6",
  author="rankmyapp",
  description="A internal logger library",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.8',
  install_requires=["requests==2.32.3", "pika==1.3.2"],
  dependency_links=[]
)
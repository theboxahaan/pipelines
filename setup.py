import setuptools

with open("README.md", 'r') as fd:
	long_description = fd.read()

setuptools.setup(
	name = "pipelines",
	version = "0.0.1",
	author = "theboxahaan",
	author_email = "ahaand@iitbhilai.ac.in",
	description = "Async Pipeline Generator",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/theboxahaan/pipelines",
	packages = setuptools.find_packages(),
	python_requires = '>=3.9',
)

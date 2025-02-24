from setuptools import setup, find_packages

setup(
    name="django-graphql-app-setup",
    version="0.1.2",
    description="A Django management command to create apps with custom folder structures for graphql APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Olatunji Komolafe",
    author_email="iamokomolafe.o.s@gmail.com",
    url="https://github.com/paisoncodes/django-graphql-app-setup",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
    ],
    python_requires=">=3.7",
)
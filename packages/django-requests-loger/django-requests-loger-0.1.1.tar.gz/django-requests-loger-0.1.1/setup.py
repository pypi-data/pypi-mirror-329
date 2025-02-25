from setuptools import setup, find_packages

setup(
    name="django-requests-loger",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "django-environ"
    ],
    include_package_data=True,
    license="MIT",
    description="A Django middleware for logging HTTP requests.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Momin Ali",
    author_email="mominalikhoker589@gmail.com",
    url="https://github.com/Momin9/django-request-logs",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)

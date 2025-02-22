from pathlib import Path

import setuptools

VERSION = "1.3.0"  # PEP-440

setuptools.setup(
    name="qbusmqttapi",
    version=VERSION,
    description="MQTT API for Qbus Home Automation.",
    url="https://github.com/Qbus-iot/qbusmqttapi",
    project_urls={
        "Source Code": "https://github.com/Qbus-iot/qbusmqttapi",
    },
    author="Koen Schockaert",
    author_email="ks@qbus.be",
    license="MIT License 2025",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={"qbusmqttapi": ["py.typed"]},
    python_requires=">=3.8",
    # Requirements
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)

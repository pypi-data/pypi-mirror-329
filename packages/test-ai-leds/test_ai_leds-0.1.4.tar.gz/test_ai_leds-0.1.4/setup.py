from setuptools import setup, find_packages

setup(
    name="test_ai_leds",
    version="0.1.4",
    author="LEDS",
    author_email="gabrieldpbrunetti@gmail.com",
    description="AI automated test generation",
    packages=find_packages(include=['testailib', 'testailib.*']),
    include_package_data=True,
    install_requires=[
        "crewai==0.86.0",
        "crewai_tools==0.17.0",
        "google_generativeai",
        "pyaml"
    ],
    entry_points={
        "console_scripts": [
            "testai=testailib.main:main",  # Executável que chama a função main
        ]
    },
)

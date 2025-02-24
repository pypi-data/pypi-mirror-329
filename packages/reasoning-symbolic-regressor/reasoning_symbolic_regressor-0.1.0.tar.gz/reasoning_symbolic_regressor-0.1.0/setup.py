from setuptools import setup, find_packages

setup(
    name="reasoning-symbolic-regressor",
    version="0.1.0",
    author="Sid Uppal",
    author_email="siddhu@gmail.com",
    description="LLM-enhanced symbolic regression: A reasoning-driven AI that refines equations using structured feedback and adaptive learning.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sidu/ReasoningSymbolicRegressor",
    packages=find_packages(),
    install_requires=[
        "pysr",
        "numpy",
        "openai",
        "pydantic"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
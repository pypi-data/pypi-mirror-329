from setuptools import setup, find_packages

setup(
    name="GPUtilSimulator",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["psutil", "setuptools"],
    author="Bryan Rocha",
    author_email="bryangomesrocha@gmail.com",
    description="A library that simulates GPUtil behavior for users without a dedicated GPU. It enables the "
                "simulation of multiple virtual GPUs, using CPU usage as a reference to generate dynamic load values. "
                "The simulated GPU usage fluctuates based on real-time CPU load, providing a realistic approximation "
                "of GPU workload behavior.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BryanRO-SpTech/GPUtilSimulator",  # URL do projeto
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

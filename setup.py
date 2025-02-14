"""setup.py for axolotl"""

import platform
from importlib.metadata import PackageNotFoundError, version
from setuptools import find_packages, setup


def parse_requirements():
    _install_requires = []
    _dependency_links = []
    with open("./requirements.txt", encoding="utf-8") as requirements_file:
        lines = [r.strip() for r in requirements_file.readlines()]
        for line in lines:
            is_extras = (
                "flash-attn" in line
                or "flash-attention" in line
                or "deepspeed" in line
                or "mamba-ssm" in line
                or "lion-pytorch" in line
            )
            if line.startswith("--extra-index-url"):
                # Handle custom index URLs
                _, url = line.split()
                _dependency_links.append(url)
            elif not is_extras and line and line[0] != "#":
                # Handle standard packages
                _install_requires.append(line)

    try:
        # detect the version of torch already installed
        # and set it so dependencies don't clobber the torch version
        torch_version = version("torch")
        _install_requires.append(f"torch=={torch_version}")
    except PackageNotFoundError:
        pass

    return _install_requires, _dependency_links


install_requires, dependency_links = parse_requirements()


setup(
    name="axolotl",
    version="0.4.1",
    description="LLM Trainer",
    long_description="Axolotl is a tool designed to streamline the fine-tuning of various AI models, offering support for multiple configurations and architectures.",
    package_dir={"": "src"},
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        "flash-attn": [
            "flash-attn==2.6.3",
        ],
        "fused-dense-lib": [
            "fused-dense-lib  @ git+https://github.com/Dao-AILab/flash-attention@v2.6.2#subdirectory=csrc/fused_dense_lib",
        ],
        "deepspeed": [
            "deepspeed==0.14.4",
            "deepspeed-kernels",
        ],
        "mamba-ssm": [
            "mamba-ssm==1.2.0.post1",
        ],
        "auto-gptq": [
            "auto-gptq==0.5.1",
        ],
        "mlflow": [
            "mlflow",
        ],
        "lion-pytorch": [
            "lion-pytorch==0.1.2",
        ],
        "galore": [
            "galore_torch",
        ],
        "optimizers": [
            "galore_torch",
            "lion-pytorch==0.1.2",
            "lomo-optim==0.1.1",
            "torch-optimi==0.2.1",
        ],
    },
)

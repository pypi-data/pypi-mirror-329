from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='mlx-lm-utils',
    url='https://github.com/JosefAlbers/mlx-lm-utils',
    py_modules=['mlx_lm_utils'],
    version='0.0.4',
    readme="README.md",
    author_email="albersj66@gmail.com",
    description="MLX-LM utils",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="MIT",
    python_requires=">=3.12.8",
    install_requires=requirements,
    # entry_points={
    #     "console_scripts": [
    #         "mlu = mlx_lm_utils:main",
    #     ],
    # },
)

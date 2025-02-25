from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="st-react-flow-pro",
    version="0.1.3",
    author="Muhammad Ahmad",
    author_email="muhammad.ahmad@redbuffer.net",
    description="Streamlit component that allows you to do X",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "jinja2"],
    package_data={
        "st_react_flow_pro": ["frontend/dist/**/*"],
    },
    exclude_package_data={
        "": ["node_modules", "*.log", "*.lock", "package.json", "package-lock.json", "tsconfig.json"]
    },
)

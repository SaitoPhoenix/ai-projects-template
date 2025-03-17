import shutil
from pathlib import Path


basic = [
    "pip",  # for installing packages
    "python-dotenv",  # for loading environment variables
    "ipykernel",  # for Interactive Jupyter notebooks
    "loguru",  # for logging
    "tqdm",  # for progress bars
    "typer",  # for building CLIs
]

notebook = [
    "ipython",  # for interactive Python
    "jupyterlab",  # for Jupyter notebooks
    "matplotlib",  # for plotting
    "notebook",  # for Jupyter notebooks
]
data_science = [
    "numpy",  # for numerical computing
    "pandas",  # for data manipulation
    "scipy",  # for scientific computing
]

machine_learning = [
    "scikit-learn",  # for machine learning
]

ai_packages_basic = [
    "pydantic",  # for data validation
    "requests",  # for making HTTP requests
    "streamlit",  # for building web apps
    "instructor",  # for training models
    "langchain",  # for chaining models
]

ai_packages_plusChunking = [
    "pydantic",  # for data validation
    "requests",  # for making HTTP requests
    "streamlit",  # for building web apps
    "instructor",  # for training models
    "langchain",  # for chaining models
    "httpx",  # for making HTTP requests
    "docling",  # for parsing HTML
    "tiktoken",  # for tokenizing text
]


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {p}" for p in packages if p not in pip_only_packages]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))


#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages_to_install = basic

# {% if cookiecutter.formatter == "ruff" %}
packages_to_install += ["ruff"]
# {% endif %} #

# {% if cookiecutter.formatter == "black" %}
packages_to_install += ["black"]
packages_to_install += ["isort"]
# {% endif %} #

# {% if cookiecutter.linter == "ruff" %}
packages_to_install += ["ruff"]
# {% endif %} #

# {% if cookiecutter.linter == "flake8" %}
packages_to_install += ["flake8"]
# {% endif %} #

# {% if cookiecutter.linter == "pylint" %}
packages_to_install += ["pylint"]
# {% endif %} #

# {% if cookiecutter.llm == "openai" %}
packages_to_install += ["openai"]
# {% endif %} #

# {% if cookiecutter.include_notebook_packages == "Yes" %}
packages_to_install += notebook
# {% endif %}

# {% if cookiecutter.include_data_science_packages == "Yes" %}
packages_to_install += data_science
# {% endif %}

# {% if cookiecutter.include_machine_learning_packages == "Yes" %}
packages_to_install += machine_learning
# {% endif %}

# {% if cookiecutter.ai_packages == "basic" %}
packages_to_install += ai_packages_basic
# {% endif %}

# {% if cookiecutter.ai_packages == "plusChunking" %}
packages_to_install += ai_packages_plusChunking
# {% endif %}

# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
# {% if cookiecutter.docs != "none" %}
packages_to_install += ["{{ cookiecutter.docs }}"]
pip_only_packages += ["{{ cookiecutter.docs }}"]
docs_subpath = docs_path / "{{ cookiecutter.docs }}"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))
# {% endif %}

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  POST-GENERATION FUNCTIONS
#
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages_to_install,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
)

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))

# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
for generated_path in Path("{{ cookiecutter.module_name }}").iterdir():
    if generated_path.is_dir():
        shutil.rmtree(generated_path)
    elif generated_path.name != "__init__.py":
        generated_path.unlink()
    elif generated_path.name == "__init__.py":
        # remove any content in __init__.py since it won't be available
        generated_path.write_text("")
# {% endif %}

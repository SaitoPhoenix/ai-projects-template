import shutil
from pathlib import Path


basic = {
    "python-dotenv": True,  # for loading environment variables
    "ipykernel": True,  # for Interactive Jupyter notebooks
    "loguru": True,  # for logging
    "tqdm": True,  # for progress bars
    "typer": True,  # for building CLIs
}

notebook = {
    "ipython": True,  # for interactive Python
    "jupyterlab": True,  # for Jupyter notebooks
    "matplotlib": True,  # for plotting
    "notebook": True,  # for Jupyter notebooks
}
data_science = {
    "numpy": True,  # for numerical computing
    "pandas": True,  # for data manipulation
    "scipy": True,  # for scientific computing
}

machine_learning = {
    "scikit-learn": True,  # for machine learning
}

ai_packages_basic = {
    "pydantic": True,  # for data validation
    "requests": True,  # for making HTTP requests
    "streamlit": True,  # for building web apps
    "instructor": True,  # for training models
    "langchain": True,  # for chaining models
}

ai_packages_plusChunking = {
    "pydantic": True,  # for data validation
    "requests": True,  # for making HTTP requests
    "streamlit": True,  # for building web apps
    "instructor": True,  # for training models
    "langchain": True,  # for chaining models
    "httpx": True,  # for making HTTP requests
    "docling": True,  # for parsing HTML
    "tiktoken": True,  # for tokenizing text
}

#
#  Packages dictionary to be used in the requirements file
#  The key is the package name and the value is a boolean
#  indicating whether the package should be installed via pip
#

packages = {}

packages["pip"] = False

# {% if cookiecutter.formatter == "ruff" %}
packages["ruff"] = True
# {% endif %} #

# {% if cookiecutter.formatter == "black" %}
packages["black"] = True
packages["isort"] = True
# {% endif %} #

# {% if cookiecutter.linter == "ruff" %}
packages["ruff"] = True
# {% endif %} #

# {% if cookiecutter.linter == "flake8" %}
packages["flake8"] = True
# {% endif %} #

# {% if cookiecutter.linter == "pylint" %}
packages["pylint"] = True
# {% endif %} #

# {% if cookiecutter.llm == "openai" %}
packages["openai"] = True
# {% endif %} #

# {% if cookiecutter.include_notebook_packages == "Yes" %}
packages.update(notebook)
# {% endif %}

# {% if cookiecutter.include_data_science_packages == "Yes" %}
packages.update(data_science)
# {% endif %}

# {% if cookiecutter.include_machine_learning_packages == "Yes" %}
packages.update(machine_learning)
# {% endif %}

# {% if cookiecutter.ai_packages == "basic" %}
packages.update(ai_packages_basic)
# {% endif %}

# {% if cookiecutter.ai_packages == "plusChunking" %}
packages.update(ai_packages_plusChunking)
# {% endif %}


# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
# {% if cookiecutter.docs != "none" %}
packages["{{ cookiecutter.docs }}"] = True
docs_subpath = docs_path / "{{ cookiecutter.docs }}"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))
# {% endif %}

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  Creating the requirements file
#

dependencies = "{{ cookiecutter.dependency_file }}"
repo_name = "{{ cookiecutter.repo_name }}"
module_name = "{{ cookiecutter.module_name }}"
python_version = "{{ cookiecutter.python_version_number }}"

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
            "  - defaults",
            "  - https://repo.anaconda.com/pkgs/main",
            "  - https://repo.anaconda.com/pkgs/r",
            "  - https://repo.anaconda.com/pkgs/msys2",
            "dependencies:",
        ]

        lines += [f"  - python={python_version}"]
        lines += [f"  - {p}" for p in sorted(packages) if not packages[p]]
        lines += ["  - pip:"]
        lines += [f"    - {p}" for p in sorted(packages) if packages[p]]
        lines += ["    - -e ."]

        f.write("\n".join(lines))

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

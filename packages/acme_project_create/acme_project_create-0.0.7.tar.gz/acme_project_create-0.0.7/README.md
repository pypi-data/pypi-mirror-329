# acme-project-create

Sets up a new (python) project using a template.

Uses a three-step process:
1. Template files are copied to the `-target-dir` location from a `--template-dir-path` directory. Default template for a python project is included in the package.
2. Directory names in the template following the pattern `{{<variable>}}` are substituted with value provided by the user.
3. Filenames in the template directory that end with `j2template` (e.g. `pyproject.toml.j2template`) are assumed to be `Jinja2` templates and a file is generated in the target location with variable substitutions provided by the user i.e. `pyproject.toml`.

And that's it.

Note: to provide all values to compile the template
the template dir needs to contain a `template_manifest.py` file that must implement a function:

`def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser`

which takes an existing instance of ArgumentParser, adds arguments specific to the template and returns the parser object.

# Default template

The default template makes several notable choices:

* Uses `venv` for virtual environments and `.venv` dir to store built environment (and `uv` to build it)
* Uses `.env` file for setting up environment variables
* Uses `setuptools` for packaging
* Uses `pytest` for testing
* Uses `mkdocs` for documentation

# Problem

Setting up all files to create a new project is time consuming and involves lots of small technical choices.

# Why use this project?

You are probably better off using [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

## Example usage

    apc -target-dir . -project-name hello-world -desc "Say hello to the world" -package-name hello_world -command hello -owner-email hello@example.com

# Project template

This project has been setup with `acme-project-create`, a python code template library.

# Required setup post use

* Enable GitHub Pages to be published via [GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
* Create `release` environment for [GitHub Actions](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment#creating-an-environment)
* Setup auth to PyPI for the GitHub Action implemented in `release.yml`: [Link](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) & uv publish [doc](https://docs.astral.sh/uv/guides/publish/#publishing-your-package)
* Once you create the python environment for the first time add the `uv.lock` file that will be created in project directory to the source control and update it each time environment is rebuilt
* Run `pre-commit install` to install the pre-commit hooks.
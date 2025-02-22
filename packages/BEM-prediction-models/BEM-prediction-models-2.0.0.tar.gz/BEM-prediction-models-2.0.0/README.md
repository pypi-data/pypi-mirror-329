# BEM Prediction Models

## Setup Instructions

Run `pip install -r requirements.txt` to install python packages.

Developed using Python version 3.9.7.

## Using this code as a library
After running the setup instructions, import the package into your code and call the
`calculate_savings(property_info)` function to calculate the savings for that property.

#### Parameters
`property_info` - a `PropertyInfo` instance.

You can find more information:

* See the [pydantic model](calculator_179d/data_types.py)
* A schema at [calculator_179d_schema.json](calculator_179d/calculator_179d_schema.json)
* The docs folder: `cd docs/` and then call `make html` or `sphinx-build -M html source/ build/` (or `make pdf`)
    * `pip install -e .[docs]` if you are missing dependencies

#### Driver program
The following is a test program you can use to check if you have correctly installed the library:

```
python examples/calculate_savings.py
```

## Running the package as a standalone application
You may run this package as a standalone application instead of importing it as a library. To do so,
simply update the parameters in `calculator_179d/calculator_user_inputs.json` and execute the code using the
following command:

```
    cd calculator_179d/
    python3 main_calculator.py calculator_user_inputs.json
```

This will create an file at `calculator_179d/output_files/calculator_outputs.json` with the results from the models.

## Development

You can do `pip install -e .[dev,docs]` to install it in editable mode, and install the necessary development and documentation dependencies such as pytest, and the pre-commit modules.

To install the pre-commit hooks, do `pre-commit install`.

## Package Releasing and Publishing

1. Merge everything to develop and then make a single merge from develop to main
1. Update package version
    * Run `bump-my-version bump patch` (possible: `major`, `minor`, `patch`, `pre_l`, `pre_n`; see `bump-my-version show-bump` beforehand).
    * This will take care of updating the various files where the version is hard-coded.
1. Make a release on GitHub (pointing to the main branch). List the updates that were made.
    * the release.yml workflow is triggered and will publish to PyPi.
    * That workflow also has a manual dispatch which will upload to TestPypi instead

Releasing manually:

1. Make the package: `python setup.py sdist`
1. Install twine (if needed):  `pip install twine`
1. Upload to pypi: `twine upload dist/<name of package you just made>`

# Overlap Integral Project

This project focuses on calculating the overlap integral between two probability density functions (PDFs). The overlap integral is a measure of similarity between two distributions and is used in various fields such as statistics, data science, etc. The code and data files in this project are designed to perform these calculations efficiently and accurately.

## Project Structure

- `src/overlap_integral/`: Contains the core Python code for calculating the overlap integral.
- `tests/`: Includes the test scripts to validate the functionality of the code.
- `README.md`: Provides an overview and instructions for the project.
- `pyproject.toml`: Configuration file for the project dependencies and metadata.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using Poetry:
    ```bash
    poetry install
    ```
4. Run the tests to ensure everything is set up correctly:
    ```bash
    poetry run make test
    ```

## Requirements

- Python 3.11 or higher
- NumPy
- SciPy
- Plotly
- Kaleido

## Usage

To calculate the overlap integral, run the following command:

```bash
poetry run python tests/test_overlap_integral.py
```

## License

This project is licensed under the MIT License.
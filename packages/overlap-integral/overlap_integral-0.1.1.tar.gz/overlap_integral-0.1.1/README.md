# Overlap Integral Project

This project focuses on calculating the overlap integral between two probability density functions (PDFs). The overlap integral is a measure of similarity between two distributions and is used in various fields such as statistics, data science, etc. The code and data files in this project are designed to perform these calculations efficiently and accurately.

## Project Structure

- `src/overlap_integral/`: Contains the core Python code for calculating the overlap integral.
- `tests/`: Includes the test scripts to validate the functionality of the code.
- `README.md`: Provides an overview and instructions for the project.
- `pyproject.toml`: Configuration file for the project dependencies and metadata.


## Installation

To install the package using `pip`, run the following command:

```bash
pip install overlap-integral
```

**Importing the Class**: Import the `OverlapIntegral` class in your Python script.

    ```python
    from overlap_integral.overlap_integral import OverlapIntegral
    ```

**Usage Example**: Provide a simple example to demonstrate how to use the `OverlapIntegral` class.

    ```python
    
            import numpy as np
            from overlap_integral.overlap_integral import OverlapIntegral

            import plotly.io as pio
            pio.kaleido.scope.default_format = "png"


            def main():
                np.random.seed(3)  # Set random seed for reproducibility

                metrics = OverlapIntegral()

                # Generate or load data
                data1 = np.random.normal(loc=30, scale=1, size=1000)
                data2 = np.random.normal(loc=30, scale=1.2, size=1000)

                # Choose PDF method: 'kde' or 'gaussian'
                pdf_method = 'gaussian'

                # Get PDFs
                pdf_1 = metrics.get_pdf(data1, method=pdf_method)
                pdf_2 = metrics.get_pdf(data2, method=pdf_method)

                # Calculate overlap integral
                lower_limit = min(np.min(data1), np.min(data2)) - 12 * max(np.std(data1), np.std(data2))
                upper_limit = max(np.max(data1), np.max(data2)) + 12 * max(np.std(data1), np.std(data2))
                integral, error = metrics.overlap_integral(pdf_1, pdf_2, lower_limit, upper_limit)

                print(f"Overlap integral: {integral}")
                print(f"Estimated error: {error}")

                # Plot distributions
                fig = metrics.plot_distributions(pdf_1, pdf_2, integral, error, x_range=(lower_limit, upper_limit))
                fig.write_image("overlap_plot.png")
                ##fig.show()

            if __name__ == '__main__':
                main()
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
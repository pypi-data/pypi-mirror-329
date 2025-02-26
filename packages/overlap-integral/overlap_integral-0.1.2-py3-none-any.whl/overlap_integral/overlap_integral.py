import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, gaussian_kde
import plotly.graph_objects as go

class OverlapIntegral:
    def __init__(self):
        pass

    def pdf_gaussian(self, x: float, mu: float, sigma: float) -> float:
        """Calculate the Gaussian PDF value at x."""
        return norm.pdf(x, mu, sigma)

    def pdf_from_kde(self, data: np.ndarray) -> callable:
        """Generate a KDE-based PDF from the input data."""
        kde = gaussian_kde(data)
        return kde

    def minimum_between_two_pdfs(self, x: float, pdf_1: callable, pdf_2: callable) -> float:
        """Calculate the minimum value between two PDFs at x."""
        if not (callable(pdf_1) and callable(pdf_2)):
            raise ValueError("Both pdf_1 and pdf_2 must be callable functions")
        return np.minimum(pdf_1(x), pdf_2(x))

    def overlap_integral(self, pdf_1: callable, pdf_2: callable, lower_limit: float, upper_limit: float) -> tuple[float, float]:
        """Calculate the overlap integral between two PDFs over a specified range."""
        if not (callable(pdf_1) and callable(pdf_2)):
            raise ValueError("Both pdf_1 and pdf_2 must be callable functions")
        integral, error = quad(lambda x: self.minimum_between_two_pdfs(x, pdf_1, pdf_2),
                               lower_limit, upper_limit)
        return integral, error

    def get_pdf(self, data: np.ndarray, method: str = 'kde', mu: float = None, sigma: float = None) -> callable:
        """
        Get a probability density function (PDF) based on the input data and method.

        Args:
            data (np.ndarray): Input data for PDF estimation.
            method (str): Method for PDF estimation. Either 'kde' or 'gaussian'.
            mu (float, optional): Mean for Gaussian distribution. Required if method is 'gaussian'.
            sigma (float, optional): Standard deviation for Gaussian distribution. Required if method is 'gaussian'.

        Returns:
            callable: A function that takes a single argument x and returns the PDF value at x.

        Raises:
            ValueError: If an unsupported PDF method is provided.
        """
        if method == 'kde':
            return self.pdf_from_kde(data)
        elif method == 'gaussian':
            if mu is None or sigma is None:
                mu, sigma = np.mean(data), np.std(data)
            return lambda x: self.pdf_gaussian(x, mu, sigma)
        else:
            raise ValueError("Unsupported PDF method. Use 'kde' or 'gaussian'.")

    def plot_distributions(self, pdf_1: callable, pdf_2: callable, integral: float, error: float, x_range: tuple = (-10, 10)) -> go.Figure:
        """Plot the distributions and their overlap."""
        x_overlap = np.linspace(x_range[0], x_range[1], 1000)
        y_pdf_1 = pdf_1(x_overlap)
        y_pdf_2 = pdf_2(x_overlap)
        y_overlap = np.minimum(y_pdf_1, y_pdf_2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_overlap, y=y_pdf_1, mode='lines', name='f(x)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x_overlap, y=y_pdf_2, mode='lines', name='g(x)', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=x_overlap, y=y_overlap, fill='tozeroy', mode='none', name=r"$\theta$", fillcolor='rgba(0,100,80,0.2)'))

        fig.update_layout(
            title=f'Overlap Integral: {integral:.4f}; \n Error: {error:.4f}',
            xaxis_title='x',
            yaxis_title='Probability Density',
            legend_title='Distributions',
        )

        fig.add_annotation(
            text=r"$\theta = \int_{-\infty}^{\infty} \min(f(x), g(x)) \, dx$",
            xref="paper",
            yref="paper",
            x=0.8,
            y=0.95,
            showarrow=False,
            font=dict(size=16)
        )

        return fig

    @staticmethod
    def load_data(data_source):
        """Load data from a given source."""
        if isinstance(data_source, (list, np.ndarray)):
            return np.array(data_source)
        elif isinstance(data_source, str):
            return np.loadtxt(data_source)
        else:
            raise ValueError("Unsupported data source type")
import torch
import inspect
from .utils import exp  # Exponential map from tangent space to hyperbolic space

class HyperbolicOptimizer:
    def __init__(self, function, D, N, optimizer=None, learning_rate=0.01):
        """
        Args:
            function (callable): The function to optimize. Takes a single (D+1, N) tensor.
            D (int): Dimension of the tangent space (D+1 in hyperbolic space).
            N (int): Number of points.
            optimizer (torch.optim.Optimizer or None): Optional optimizer, default Adam.
            learning_rate (float): Learning rate for optimization.
        """
        self.function = function
        self.D = D  # Tangent space dimension
        self.N = N  # Number of points
        self.learning_rate = learning_rate
        self.optimizer = optimizer  # Custom optimizer or None (default)

    def optimize(self, epochs=100):
        """
        Optimize a function in hyperbolic space.

        Args:
            epochs (int): Number of optimization steps.

        Returns:
            torch.Tensor: Optimized points in hyperbolic space (D+1, N).
        """
        # Initialize optimization variables in tangent space (D, N)
        variables = torch.nn.Parameter(torch.randn(self.D, self.N) * 0.01)

        # Default optimizer: Riemannian Gradient Descent
        optimizer = self.optimizer([variables]) if self.optimizer else torch.optim.Adam([variables], lr=self.learning_rate)

        for epoch in range(epochs):
            optimizer.zero_grad()
            hyperbolic_points = exp(variables)  # Convert (D, N) to (D+1, N)
            loss = self.function(hyperbolic_points)  # Evaluate function
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch}: Loss = {loss.item()}")

        return exp(variables).detach()  # Return optimized points in hyperbolic space

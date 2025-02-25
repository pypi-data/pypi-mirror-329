import numpy as np
import pandas as pd
from skfolio import Portfolio as BasePortfolio


class Portfolio(BasePortfolio):
    @property
    def all_weights_per_observation(self) -> pd.DataFrame:
        """DataFrame of the Portfolio weights containing even near zero weight per observation."""
        weights = self.weights
        assets = self.assets
        df = pd.DataFrame(
            np.ones((len(self.observations), len(assets))) * weights,
            index=self.observations,
            columns=assets,
        )
        return df

    def get_next_weights(self, returns: pd.Series) -> dict[int, float]:
        """
        Given the next returns, compute the next weights of this portfolio

        Args:
            returns: The returns for the next day as a pandas series

        Returns:
            A dictionary of weights (instrument ids as keys and weights as values)
        """
        weights = self.all_weights_per_observation.iloc[-1, :].T
        if weights.sum() != 0:
            weights /= weights.sum()
        contribution = weights * (returns + 1.0)
        if contribution.sum() != 0:
            contribution /= contribution.sum()
        return contribution.dropna().to_dict()

    def get_estimate_net_value(self, previous_net_asset_value: float) -> float:
        if self.previous_weights is None:
            raise ValueError("No previous weights available")
        expected_returns = self.previous_weights @ self.X.iloc[-1, :].T
        return previous_net_asset_value * (1.0 + expected_returns)

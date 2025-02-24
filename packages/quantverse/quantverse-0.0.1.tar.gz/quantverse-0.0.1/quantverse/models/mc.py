import numpy as np
import pandas as pd

from quantverse.core.model import Model
from quantverse.models.brownian import BrownianMotion
from quantverse.util import from_obj, values, array


class MonteCarlo(Model):

    @staticmethod
    def simulate(S, K, sigma, r, t, T, n_samples=100_000, seed=1) -> dict:
        f = lambda x: array(x)[None, :].repeat(n_samples, axis=0)
        dt = T-t
        log_returns = BrownianMotion.formula(f(r), f(sigma), f(dt), seed=seed)
        St = S * np.exp(log_returns)

        payoff = np.maximum(0, St - K)
        C = np.exp(-r * dt) * np.mean(payoff, axis=0)
        return dict(C=C)

    @staticmethod
    def run(*args, **kwargs) -> dict:
        return MonteCarlo.simulate(*args, **kwargs)

    def predict(self,
                data: pd.DataFrame,
                asset_price: str = 'S',
                strike_price: str = 'K',
                volatility: str = 'sigma',
                risk_free_rate: str = 'r',
                time: str = 't',
                time_to_expiration: str = 'T',
                **kwargs) -> dict:
        S, K, sigma, r, t, T = from_obj(data, asset_price, strike_price, volatility,
                                        risk_free_rate, time, time_to_expiration, f=values)
        return MonteCarlo.run(S, K, sigma, r, t, T, **kwargs)

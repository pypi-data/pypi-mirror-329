import numpy as np
import pandas as pd
from numpy.random import RandomState

from quantverse.core.model import Model
from quantverse.util import from_obj, nvl, values, get


class BrownianMotion(Model):

    @staticmethod
    def formula(mu, sigma, dt, random_state=None, seed=None) -> dict:
        random_state = nvl(random_state, RandomState(seed))
        z = random_state.normal(loc=0, scale=1, size=get(mu + sigma, 'shape'))
        return (mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z

    @staticmethod
    def simulate(mu, sigma, dt, S=1.0, random_state=None, seed=None) -> dict:
        log_returns = BrownianMotion.formula(mu, sigma, dt, random_state=random_state, seed=seed)
        returns = np.exp(np.cumsum(log_returns))
        St = S * returns
        return dict(log_returns=log_returns, returns=returns, St=St, t=np.cumsum(dt))

    @staticmethod
    def run(*args, **kwargs) -> dict:
        return BrownianMotion.simulate(*args, **kwargs)

    def predict(self,
                data: pd.DataFrame,
                drift: str = 'mu',
                volatility: str = 'sigma',
                asset_price: str = 'S',
                time_step: str = 'dt',
                **kwargs) -> dict:
        mu, sigma, dt, S = from_obj(data, drift, volatility, time_step, asset_price, f=values)
        return BrownianMotion.run(mu, sigma, dt, S=nvl(S, 1.0), **kwargs)




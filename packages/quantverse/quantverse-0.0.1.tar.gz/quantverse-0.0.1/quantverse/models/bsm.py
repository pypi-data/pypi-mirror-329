import numpy as np
import pandas as pd
from scipy import stats

from quantverse.core.model import Model
from quantverse.util import from_obj, values


class BlackScholesModel(Model):

    @staticmethod
    def formula(S, K, sigma, r, t, T):
        d1 = (np.log(S / K) + (r + ((sigma ** 2) / 2)) * (T - t)) / (sigma * np.sqrt((T - t)))
        d2 = d1 - sigma * np.sqrt((T - t))
        C = S * stats.norm.cdf(d1) - K * np.exp(-r * (T - t)) * stats.norm.cdf(d2)
        return dict(d1=d1, d2=d2, C=C)

    @staticmethod
    def run(*args, **kwargs):
        return BlackScholesModel.formula(*args, **kwargs)

    def predict(self,
                data: pd.DataFrame,
                asset_price: str = 'S',
                strike_price: str = 'K',
                volatility: str = 'sigma',
                risk_free_rate: str = 'r',
                time: str = 't',
                time_to_expiration: str = 'T') -> dict:
        S, K, sigma, r, t, T = from_obj(data, asset_price, strike_price, volatility,
                                        risk_free_rate, time, time_to_expiration, f=values)
        return BlackScholesModel.run(S, K, sigma, r, t, T)

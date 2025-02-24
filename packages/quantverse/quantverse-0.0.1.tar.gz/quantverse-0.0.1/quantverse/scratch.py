import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from models.brownian import BrownianMotion
from models.bsm import BlackScholesModel
from models.mc import MonteCarlo
from util.builder import Builder


def plot_brownian_motion():
    df = (Builder()
          .add(mu=.06)
          .add(sigma=.3)
          .add(dt=0.01 * np.ones(100))
          .add(sample=np.arange(100))
          .add(S=100)
          .build()
          .groupby('sample', as_index=False)
          .apply(BrownianMotion().transform)
          )

    print(df)

    sns.lineplot(data=df, x='t', y='St', hue='sample', color='black')
    plt.xlabel('t')
    plt.ylabel('St')
    plt.show()


plot_brownian_motion()


def plot_option_prices_by_strike():
    df = (Builder()
          .add(S=[95, 98, 100, 103, 105])
          .add(K=100)
          .add(sigma=.3)
          .add(r=.06)
          .add(t=np.arange(0.75, 1.0, 0.01))
          .add(T=1.0)
          .pipe(BlackScholesModel(prefix='exact_').transform)
          .pipe(MonteCarlo(prefix='mc_').transform)
          )

    sns.lineplot(data=df, x='t', y='exact_C', hue='S')
    sns.scatterplot(data=df, x='t', y='mc_C', hue='S', color='black')
    plt.xlabel('t')
    plt.ylabel('C')
    plt.ylim(-0.5, 8)
    plt.show()


plot_option_prices_by_strike()


def plot_option_prices_by_asset_price():
    df = (Builder()
          .add(S=np.arange(95, 105, 0.5))
          .add(K=100)
          .add(sigma=.3)
          .add(r=.06)
          .add(t=.999999)
          .add(T=1.0)
          .build()
          .pipe(BlackScholesModel(prefix='exact_').transform)
          .pipe(MonteCarlo(prefix='mc_').transform)
          )

    sns.lineplot(data=df.dropna(), x='S', y='exact_C')
    sns.scatterplot(data=df, x='S', y='mc_C', color='black')
    plt.xlabel('S')
    plt.ylabel('C')
    plt.show()


plot_option_prices_by_asset_price()

S = 105
K = 100
sigma = 0.3
r = 0.06
t = .9999
T = 1.0

print('Exact: ', BlackScholesModel().run(S, K, sigma, r, t, T)['C'])
print('Monte Carlo:', MonteCarlo().run(S, K, sigma, r, t, T)['C'])

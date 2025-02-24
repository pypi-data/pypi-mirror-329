import pandas as pd


class Model:

    def __init__(self, prefix=None):
        super().__init__()
        self.prefix = prefix

    def predict(self, data: pd.DataFrame, *args, **kwargs) -> dict:
        pass

    def transform(self, data, **kwargs) -> pd.DataFrame:
        res = self.predict(data, **kwargs)
        if self.prefix is not None:
            res = {self.prefix + k: v for k, v in res.items()}
        return data.assign(**res)

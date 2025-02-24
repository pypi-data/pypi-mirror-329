from typing import Iterable

import pandas as pd


class Builder:

    def __init__(self):
        super().__init__()
        self.labels = []
        self.values = []

    def add(self, **kwargs):
        for k, v in kwargs.items():
            self.labels.append(k)
            if not isinstance(v, Iterable):
                v = [v]
            self.values.append(v)

        return self

    def build(self):
        index = pd.MultiIndex.from_product(self.values, names=self.labels)
        return pd.DataFrame(index=index).reset_index()

    def pipe(self, f, *args, **kwargs):
        return f(self.build(), *args, **kwargs)

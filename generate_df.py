import pandas as pd
import numpy as np


def generate_test_dataframe(n=1000):

    # base dataframe
    df = pd.DataFrame({'yv1': 100 + 10*np.random.randn(n),
                       'cv1': pd.Categorical(np.random.choice(list('ABCDEFG'), n), ordered=True),
                       'bv1': np.random.choice(a=[np.nan, 1], size=n, replace=True, p=[0.1, .90])})

    # interactions. x2 depends on the levels of c1.
    df['yv2'] = np.cos(df['cv1'].cat.codes)*5 + df['yv1']

    # now make x3 the same as x2,  but with the random missing values (real world,  we have missing data)
    df['yv3'] = df['yv2'] * df['bv1']

    return df


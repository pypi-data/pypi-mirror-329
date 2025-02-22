import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
def mice(df, max_iter=10):
    mice_imputer = IterativeImputer(random_state=42, sample_posterior=True, max_iter=max_iter)
    data_mice = pd.DataFrame(mice_imputer.fit_transform(df), columns=df.columns)
    return data_mice
import pandas as pd
from sklearn.impute import IterativeImputer
def sice(df , max_iter : 10):
    sice_imputer = IterativeImputer(random_state=42, sample_posterior=False, max_iter=max_iter)
    data_sice = pd.DataFrame(sice_imputer.fit_transform(df), columns=df.columns)
    return data_sice
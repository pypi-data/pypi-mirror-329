import pandas as pd
from fancyimpute import IterativeImputer as EMImputer
def em(df):
    em_imputer = EMImputer()
    data_em = pd.DataFrame(em_imputer.fit_transform(df), columns=df.columns)
    return data_em
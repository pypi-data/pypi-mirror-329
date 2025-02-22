import pandas as pd
oheMap_encode ,oheMap_decode  = {} , {}

def encode(df , cat_cols):
    for col in cat_cols:
        vals = df[col].value_counts()
        vals = [(freq, char) for char, freq in vals.items()]
        vals.sort()
        oheMap_encode[col] = {}
        oheMap_decode[col] = {}
        for i in range(len(vals)):
            char = vals[i][1]
            oheMap_encode[col][char] = i+1
            oheMap_decode[col][i+1] = char
        
        df[col] = df[col].apply(lambda x: oheMap_encode[col][x] if not pd.isna(x) else x)




def decode(df , cat_cols):
    for col in cat_cols:
        df[col] = df[col].apply(lambda x: oheMap_decode[col][x] if not pd.isna(x) else x)
        

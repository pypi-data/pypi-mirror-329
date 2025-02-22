import pandas as pd
import numpy as np
from .getClusters import getClusters
from clustered_imputation.dummyData import data
from typing import Literal
from clustered_imputation.basicImputer import mice , sice , em
from clustered_imputation.clusterBase import encode , decode

class clusterImputer:
    def __init__(self , data ,basic_imputation : Literal["mice" , "sice" , "em"] , num_imputation : Literal["mean" , "median"] , 
            corr_threshold : 0.6 , max_iter : 10):
        self.df = data
        self.basic_imputation = basic_imputation
        self.num_imputation = num_imputation
        self.corr_threshold = corr_threshold   
        self.max_iter = max_iter
        self.num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist()

    def impute(self):
        encode(self.df , self.cat_cols)
        clusters = getClusters(self.df , self.num_imputation , self.corr_threshold  , self.num_cols , self.cat_cols)
        dataFrames = []
        for cluster in clusters:
            df_cl = self.df[cluster]
            if self.basic_imputation == "mice":
                df_cl = mice(df_cl ,self.max_iter)
            elif self.basic_imputation == "sice":
                df_cl = sice(df_cl , self.max_iter)
            else:
                df_cl = em(df_cl)
            dataFrames.append(df_cl)

        ans = dataFrames[0]
        for i in range(1 , len(dataFrames)):
            ans = pd.concat([ans , dataFrames[i]] , axis = 1)
        decode(ans  , self.cat_cols)
        self.df.loc[:, :] = ans

    
# testing
from typing import Literal
import numpy as np
from clustered_imputation.clusterBase import cluster_features


def getClusters(df, num_imputation: Literal["mean", "median"], corr_threshold : 0.6 , num_cols , cat_cols):
    df_copy = df
    for col in num_cols:
        if num_imputation == "mean":
            x = df_copy[col].mean()
        else:
            x = df_copy[col].median()
        df_copy[col] = df_copy[col].fillna(x)
    for col in cat_cols:
        x = df_copy[col].mode()[0]
        df_copy[col] = df_copy[col].fillna(x)
    clusters = cluster_features(df_copy, corr_threshold=corr_threshold)
    finalClusters = []
    single = []
    for cluster in clusters:
        if len(cluster) > 1:
            finalClusters.append(cluster)
        else:
            single.append(cluster[0])
    finalClusters.append(single)
    return finalClusters

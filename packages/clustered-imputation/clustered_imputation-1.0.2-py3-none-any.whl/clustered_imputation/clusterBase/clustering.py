def cluster_features(df, corr_threshold = 0.6):
    corr_matrix = df.corr().abs()  # absolute correlation matrix
    clusters = []  # list of clusters
    visited = set()

    for col in corr_matrix.columns:
        if col in visited:
            continue
        # Start a new cluster and add the current column if it has correlated columns
        cluster = [col]
        for other_col in corr_matrix.columns:
            if other_col not in visited and other_col != col and corr_matrix[col][other_col] > corr_threshold:
                cluster.append(other_col)
                visited.add(other_col)
        visited.add(col)  # Mark the current column as visited
        clusters.append(cluster)  # Only add non-empty clusters

    #print(clusters)
    return clusters
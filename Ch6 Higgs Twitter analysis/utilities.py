import numpy as np

def normalize_pandas_column(df, column):
    return (df[column] - df[column].min()) / (df[column].max() - df[column].min())

def normalize_pandas_dataframe(df, column):
    return (df[column] - df.min().min()) / (df.max().max() - df.min().min())

def list_of_values(dict):
    return [dict[key] for key in dict.keys()]

def top_nodes(df_centralities, df_column_names , n = 1000):
    top_nodes_set = set(df_centralities.sort_values(by=df_column_names[0], ascending=False).head(1000)['nodeId'])
    for column_name in df_column_names[1:]:
        top_nodes_set = top_nodes_set.union(set(df_centralities.sort_values(by=column_name, ascending=False).head(1000)['nodeId']))

def normalize_vector(v):
    """
        Normalize vector

        normalized_v = v / ||v||

        where ||v|| : 2-norm of vector v
    """
    return v/np.linalg.norm(v)

def factor_vector(v, factor):
    """
        Multiply scalar with vector:    a * v
    """
    return factor * np.array(v)
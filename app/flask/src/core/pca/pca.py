import pandas as pd


def get_df():
    df = pd.DataFrame({'a': [1, 2 , 3], 'b': ['aloha', 'mahalo', 'hawaii']})

    return {
        'geo_heatmap': {'df': df}
    }
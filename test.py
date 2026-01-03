from jupyter_server.utils import fetch
from sklearndemo.src.fetch_data import FetchedData
from sklearn.datasets import load_iris
import pandas as pd

if __name__ == '__main__':
    iris=load_iris()
    iris_df_features = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    FetchedData.export_data(iris_df_features)
import pandas as pd


class DataFrameHelper:
    def __init__(self, data: dict):
        self.data = data
        self.df = pd.DataFrame(data)

    def filter_columns(self, columns: list):
        self.df = self.df[columns]
        return self

    def query_rows(self, condition: str):
        self.df = self.df.query(condition)
        return self

    def drop_columns(self, columns: list):
        self.df = self.df.drop(columns=columns)
        return self

    def skip_rows(self, n: int):
        self.df = self.df.iloc[n:]
        return self

    def reset_index(self):
        self.df.reset_index(drop=True, inplace=True)
        return self

    def to_dict(self):
        return self.df.to_dict(orient='records')

    def to_dataframe(self):
        return self.df


if __name__ == "__main__":
    data = {
        "name": ["John", "Alice", "Bob"],
        "age": [25, 24, 26],
        "city": ["New York", "Los Angeles", "Chicago"]
    }
    df_helper = DataFrameHelper(data)
    df = df_helper.filter_columns(["name", "city"]).to_dataframe()
    print(df)
    print(df_helper.to_dict())
    print(df_helper.skip_rows(1).to_dict())
    print(df_helper.reset_index().to_dict())
    print(df_helper.drop_columns(["city"]).to_dict())
    print(df_helper.to_dict())
    print(df_helper.to_dataframe())

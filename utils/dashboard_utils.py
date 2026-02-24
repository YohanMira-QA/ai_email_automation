import pandas as pd

def prepare_download(df):

    df_sorted = df.sort_values(by="category")

    df_sorted = df_sorted[[
        "email_body",
        "category",
        "auto_response"
    ]]

    df_sorted.columns = [
        "Email",
        "Category",
        "Auto_Response"
    ]

    return df_sorted
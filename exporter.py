import pandas as pd
from config import OUTPUT_FILE

def export_results(dataframe):
    dataframe.to_excel(OUTPUT_FILE, index=False)
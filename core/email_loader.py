import pandas as pd
import os

def load_emails(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    df = pd.read_csv(file_path)
    
    if df.empty:
        raise ValueError("El archivo CSV está vacío.")
    
    return df
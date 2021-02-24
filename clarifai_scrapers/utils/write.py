# SYSTEM IMPORTS
import pandas as pd


def write_data_to_csv(data: list, output: str):
    df = pd.DataFrame(data)
    df.to_csv(output, index=False)
    print(f'Results saved to output file: {output}')
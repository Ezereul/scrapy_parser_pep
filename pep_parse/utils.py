import glob
import os.path

import pandas as pd


def rename_first_row():
    files = glob.glob('results/pep_*.csv')
    file = max(files, key=os.path.getctime)

    df = pd.read_csv(file)
    df.rename(columns={'number': 'Номер',
                       'name': 'Название',
                       'status': 'Статус'})
    df.to_csv(file, index=False)

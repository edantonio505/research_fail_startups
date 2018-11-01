import requests
from bs4 import BeautifulSoup
import pandas as pd

# ===================================================================
#      HELPER FUNCTION TRANSFORMS BEAUTIFULSOUP OBJECTS TO DATAFRAMES
# ===================================================================
def get_df(tr_array):
    dataset = []
    for tr in tr_array:
        tds = tr.find_all('td')
        columns = []
        for td in tds:
            columns.append(td.text)
        dataset.append(columns)
    columns = dataset[1]
    dataset = dataset[2:]
    return pd.DataFrame(dataset, columns=columns)





# ====================================================================
#           Main Function
# ====================================================================
def main():
    base = "http://autopsy.io"
    directory_save = "datasets/"
    file_name = "autopsyio_dataset.csv"
    r = requests.get(base)
    soup =  BeautifulSoup(r.text, 'html.parser')
    tr_array = soup.find_all('tr')
    df = get_df(tr_array)
    print(df)
    try:    
        print("Dataset saved successfuly")
        df.to_csv("{}/{}".format(directory_save, file_name))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
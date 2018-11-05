import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# ===================================================================
#      HELPER FUNCTION TRANSFORMS BEAUTIFULSOUP OBJECTS TO DATAFRAMES
# ===================================================================
def get_df(tr_array):
    dataset = []

    for tr in tr_array:
        tds = tr.find_all('td')
        columns = []        
        links = []

        for td in tds:
            columns.append(td.text)
        
        for i in range(len(tds)):
            td = tds[i]
            link = ""
            # I have to see what other data I can get from here!
            #  get startup url if there is a url
            if i == 1:
                try:
                    link = [x.get('href') for x in td.find_all('a')][0]
                except:
                    link = ""
                links.append(link)

            # Full Story link
            if i == 4:
                try: 
                    link = [x.get('href') for x in td.find_all('a')][0]
                except:
                    link = "" 
                links.append(link)

            # Getting founder link
            if i == 5:
                try :   
                    link = [x.get('href') for x in td.find_all('a')][0]
                except:
                    link = "" 
                links.append(link)        

        columns = columns + links
        dataset.append(columns)
    columns = dataset[1]
    columns[6] = "Startup_link"
    columns[7] = "Full_story_link"
    columns[8] = "Founder_link"
    columns = [x.replace(" ", "_") for x in columns]
    dataset = dataset[2:]
    return pd.DataFrame(dataset, columns=columns)





# ====================================================================
#           Main Function
# ====================================================================
def main():
    base = "http://autopsy.io"
    path = str(os.getcwd()).replace("data_collectors", "")
    directory_save = "{}datasets/autopsy_io/".format(path)
    file_name = "failed_companies_autopsyio_dataset.csv"
    r = requests.get(base)
    soup =  BeautifulSoup(r.text, 'html.parser')
    tr_array = soup.find_all('tr')
    df = get_df(tr_array)
    print(df)
    try:    
        print("Dataset saved successfuly")
        df.to_csv("{}/{}".format(directory_save, file_name), index=False)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

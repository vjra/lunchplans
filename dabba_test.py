import wget
import os,sys
import camelot # extracts tables from pdf
import pandas as pd

pd.options.display.max_colwidth = 150


def filedownload_n_extract_table(url,filename):
    """Downloads a pdf file from url and saves it to filename.
        Convertes the pdf file to a pandas table, using the package camelot.


    Parameters:
    url (str): url that contains a pdf.
    filename (str): Filename for local pdf.

    Returns:
    table (pd.Dataframe): Extracted table from the pdf file.
    """
    wget.download(url,filename)
    table = camelot.read_pdf(filename,flavor='stream')
    return table

def dabba_clean_export(url,filename='dabba.pdf',datestamp = ''):
    """Downloads, trims and cleanes table from a extracted pdf.
    Exports the file into two csv files. One with the datestamp appended.


    Parameters:
    url (str): url that contains a pdf.
    filename (str): Filename for local pdf.
    datestamp (str): Is appended onto one of the csv exports.

    Returns:
    df_clean (pd.Dataframe): Extracted table from the pdf file, cleaned and trimmendself.
    """
    ############################################################################
    ########################## Download table and extract ######################
    ############################################################################
    table = filedownload_n_extract_table(url,filename)

    ############################################################################
    ########################## Data Wrangling and cleaning #####################
    ############################################################################

    df = pd.DataFrame(table[0].df)
    df.drop([0,2,4,7,10,13,16],axis=0, inplace = True)
    df.reset_index(drop = True,inplace = True)
    df.drop(0,axis=1, inplace = True)
    df[df.index % 2 ==0] = ' '+df[df.index % 2 ==0]
    for i in [1,3,5,7,9]:
        df.iloc[i,:] = df.iloc[i,:]+df.iloc[i+1,:]

    df.drop([2,4,6,8,10],axis=0, inplace = True)
    df.reset_index(drop = True,inplace = True)
    df_clean =df
    print(df)
    # df.iloc[1:,:] = df.iloc[1:,:].applymap(lambda x: x.replace('-',''))
    # df_clean = df.copy()
    #
    # df_clean.index = ['Weekmenu','Mo','Tue','Wed','Thu','Fr']
    # df_clean.columns = ['M1','M2','M3']

    ############################################################################
    ########################## Export ##########################################
    ############################################################################
    # df_clean.to_csv('./datasets/df_clean_{}.csv'.format(datestamp), index = False)
    # df_clean.to_csv('./datasets/df_clean_actual.csv', index = False)
    return df_clean

# os.remove('dabba.pdf')
fileurl = 'https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.pdf'
df_clean = dabba_clean_export(fileurl,'dabba.pdf')

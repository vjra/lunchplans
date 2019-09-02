from flask import Flask, render_template, url_for
from multiprocessing import Value
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import wget
import os,sys
import camelot # extracts tables from pdf
import pandas as pd
from PIL import Image

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
    df.iloc[1:,:] = df.iloc[1:,:].applymap(lambda x: x.replace('-',''))
    df_clean = df.copy()

    df_clean.index = ['Weekmenu','Mo','Tue','Wed','Thu','Fr']
    df_clean.columns = ['M1','M2','M3']

    ############################################################################
    ########################## Export ##########################################
    ############################################################################
    df_clean.to_csv('./datasets/df_clean_{}.csv'.format(datestamp), index = False)
    df_clean.to_csv('./datasets/df_clean_actual.csv', index = False)
    return df_clean


# Flask is a class, so its in upper case
app = Flask(__name__)

def get_date_function():
    """Returns name, date and calender week of current day.

    Returns:
    weekdayname,date,kw: weekdayname (str),date (str),kw (str)


    """

    today = datetime.now()
    weekdayname = today.strftime("%A")
    date = str(today.date())
    kw = str(today.isocalendar()[1])
    return weekdayname,date,kw

def how_old_is_the_filedate(filename):
    """Checks the age of a file in the current folder.

    Parameters:
    filename (str): Filename in folder.

    Returns:
    difftime.days (int): Number of days since the file has been modified.
    """
    t = os.path.getmtime(filename)
    difftime = datetime.now() - datetime.fromtimestamp(t)
    return difftime.days

def filedownloado(url,filename):
    wget.download(url,filename)

def dabbajpgcutter():
    box = (46,46,1195,632)
    mo_box = (120,230,1146,286)
    tue_box = (120,230+80,1146,286+80)
    wed_box = (120,230+80*2,1146,286+80*2)
    thu_box = (120,230+80*3,1146,286+80*3)
    fri_box = (120,230+80*4,1146,286+80*4)
    boxes = [mo_box,tue_box,wed_box,thu_box,fri_box]
    regions = []
    with Image.open('dabba.jpg') as im:
        print(im.format, im.size, im.mode)
        all_region = im.crop(box)
        for box in boxes:
            temp = im.crop(box)
            m1 = temp.crop([0,0,342,56])
            m2 = temp.crop([342,0,342*2,56])
            m3 = temp.crop([342*2,0,342*3,56])
            regions.append([m1,m2,m3])

    for j in range(0,5):
        filename = '{}'.format(j)
        for i in range(0,3):
            regions[j][i].save('static/dabba_cuttings/'+filename+'{}'.format(i)+'.png', "PNG")

try:
    difftime = how_old_is_the_filedate('dabba.pdf')
except:
    difftime = how_old_is_the_filedate('dabba.jpg')

weekdayname,date,kw = get_date_function()

############################################################################
################ Filling in html files and scrap data ######################
############################################################################

@app.route('/')
def home():
    """Webscrapes the following pages or pdfs for lunch menus:
    * https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.pdf
    * http://www.feinessen.at/
    * https://www.bep-viet.at/
    * http://teigware.at

    And generates template data for the html files.
    """
    ############################################################################
    ############################## Dabba scraping ##############################
    ############################################################################
    # looks up the time, how long dabba.jpg was not modified
    # if its longer then 6 days, it downloads
    try:
        if difftime >=6:
            date2 = date.replace('-','_')
            os.remove('dabba.pdf')
            fileurl = 'https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.pdf'
            dabba_clean_export(fileurl,'dabba.pdf',datestamp = date2)

        df_dabba = pd.read_csv('./datasets/df_clean_actual.csv')
        dabba_weekmenu = df_dabba['M1'][0]
        df_dabba_m = df_dabba.iloc[1:,:].copy()
        df_dabba_m.index = ['Mo','Tue','Wed','Thu','Fr']
        pandas_cutting_switch = True
    except:
        os.remove('dabba.jpg')
        fileurl = 'https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.jpg'
        filedownloado(fileurl,'dabba.jpg')
        dabbajpgcutter()
        pandas_cutting_switch = False
        print("Unexpected error:", sys.exc_info()[0])
        dabba_weekmenu = 'dabba week menu'
        df_dabba_m = pd.DataFrame(columns=['something', 'went', 'wrong'])
        df_dabba = df_dabba_m

    ############################################################################
    ############################## Feinessen scraping ##########################
    ############################################################################
    try:
        hplink = 'http://www.feinessen.at/'
        page = urllib.request.urlopen(hplink)
        soup = BeautifulSoup(page, 'html.parser')
        paragraphs = soup.find_all('p')
        h3s = soup.find_all('h3')
        listofinterest = [2,3,4,10,11,12,17,18,19,22,23,24,27,28,29]
        listofh3s = [1]
        feinessentemp = ''
        feinessenmenu = []
        j = 0
        for i in listofinterest:
            feinessentemp = feinessentemp + paragraphs[i].text
            j += 1
            if j % 3==0:
                feinessenmenu.append(feinessentemp)
                feinessentemp = ''
    except:
        feinessenmenu = []
        print("Unexpected error:", sys.exc_info()[0])
        for i in range(0,5):
            feinessenmenu.append('Kein Eintrag')

    ############################################################################
    ############################## Bepviet scraping ############################
    ############################################################################
    try:
        hplink = 'https://www.bep-viet.at/'
        page = urllib.request.urlopen(hplink)
        soup = BeautifulSoup(page, 'html.parser')
        h4s = soup.find_all('h4')
        divs = soup.find_all('div', {"class": "fh5co-food-pricing"})
        beblist = []
        j=0
        for i in h4s:
            beblist.append(i.text+divs[j].text)
            j+=1
    except:
        beblist = []
        print("Unexpected error:", sys.exc_info()[0])
        for i in range(0,5):
            beblist.append('Kein Eintrag')

    ############################################################################
    ############################## teigware scraping ###########################
    ############################################################################
    try:
        hplink = 'http://teigware.at'
        page = urllib.request.urlopen(hplink)
        soup = BeautifulSoup(page, 'html.parser')
        divs = soup.find_all('td', {"class": "textcenter"})
        teigware = []
        teigwaretemp = ''
        teigware = []
        teigwaretemp = ''
        for i in range(0,11,1):
            if i % 2 == 0 and i != 0:
                teigware.append(teigwaretemp)
                teigwaretemp = ''
            if teigwaretemp != '':
                teigwaretemp = teigwaretemp + ' M2: ' +divs[i].text
            else:
                teigwaretemp = 'M1: ' + divs[i].text
    except:
        teigware = []
        for i in range(0,5):
            teigware.append('Kein Eintrag')

        print("Unexpected error:", sys.exc_info()[0])
    ############################################################################
    ##################### Generate template data for html ######################
    ############################################################################
    version = 'v0.05'
    currentweekday = datetime.today().weekday()
    templateData = {
    'pandas_cutting_switch' : pandas_cutting_switch,
    'currentday' : currentweekday,
    'weekdayname':weekdayname,
    'date': date,
    'weeknumber': kw,
    'dabba_weekmenu' : dabba_weekmenu,
    'versionname' : version,
    'feinessen0' : feinessenmenu[0],
    'feinessen1' : feinessenmenu[1],
    'feinessen2' : feinessenmenu[2],
    'feinessen3' : feinessenmenu[3],
    'feinessen4' : feinessenmenu[4],
    'beb0' : beblist[0],
    'beb1' : beblist[1],
    'beb2' : beblist[2],
    'beb3' : beblist[3],
    'beb4' : beblist[4],
    'teig0' : teigware[0],
    'teig1' : teigware[1],
    'teig2' : teigware[2],
    'teig3' : teigware[3],
    'teig4' : teigware[4],
    }
    return render_template("home.html", **templateData, tables=[df_dabba_m.to_html(classes='data',justify='center')], titles=df_dabba.columns.values)


@app.route('/about')
def about():
    ############################################################################
    ##################### Generate template data for html ######################
    ############################################################################
    templateData = {
    'weekdayname':weekdayname,
    'date': date,
    'weeknumber': kw}
    return render_template("about.html", **templateData)

@app.route('/others')
def others():
    ############################################################################
    ##################### Generate template data for html ######################
    ############################################################################
    templateData = {
    'weekdayname':weekdayname,
    'date': date,
    'weeknumber': kw}
    return render_template("other_loc.html", **templateData)


if __name__=="__main__":
    app.run(debug=True)

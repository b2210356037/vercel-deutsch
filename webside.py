from flask import Flask, render_template, request
#from ponsScrap2 import Scraper, Maker, Reverso
from bs4 import BeautifulSoup
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def Reverso(istek):
    data = []
    url = f"https://context.reverso.net/translation/german-english/{istek}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tablesDE = soup.find_all("div", class_="src ltr")
    tablesEN = soup.find_all("div", class_="trg ltr")

    c = 0
    for index in range(len(tablesDE)):
        if(c == 10):
            break
        textDE = tablesDE[index].find("span", class_="text").text
        textEN = tablesEN[index].find("span", class_="text").text
        textDEEM = tablesDE[index].find("em").text
        textENEM = tablesEN[index].find("em").text
        # f.write(textDE + "( "+ f"{textDEEM}" + " )" )
        # f.write(textEN + "( " + f"{textENEM}" + " )")
        # f.write("\n")
        c += 1
        data.append([textDE, textDEEM, textEN, textENEM])
    return data

def Maker(istek, data):
    try:
        result = ""
        for i in range(15):
            if i == 0:
                col_names = ["Personel Pronomen", "Präsens"]
                karts = data[0:6]
            elif i == 1:
                col_names = ["Personel Pronomen", "Präteritum"]
                karts = data[6:12]
            elif i == 2:
                col_names = ["Personel Pronomen", "Perfekt"]
                karts = data[12:18]
            elif i == 3:
                col_names = ["Personel Pronomen", "Plusquamperfekt"]
                karts = data[18:24]
            elif i == 4:
                col_names = ["Personel Pronomen", "Futur I"]
                karts = data[24:30]
            elif i == 5:
                col_names = ["Personel Pronomen", "Futur II"]
                karts = data[30:36]
            elif i == 6:
                col_names = ["Personel Pronomen", "Konjunktiv I - Präsens"]
                karts = data[36:42]
            elif i == 7:
                col_names = ["Personel Pronomen", "Konjunktiv I - Perfekt"]
                karts = data[42:48]
            elif i == 8:
                col_names = ["Personel Pronomen", "Konjunktiv I - Futur I"]
                karts = data[48:54]
            elif i == 9:
                col_names = ["Personel Pronomen", "Konjunktiv I - Futur II"]
                karts = data[54:60]
            elif i == 10:
                col_names = ["Personel Pronomen", "Konjunktiv II - Präteritum"]
                karts = data[60:66]
            elif i == 11:
                col_names = ["Personel Pronomen", "Konjunktiv II - Plusquamperfekt"]
                karts = data[66:72]
            elif i == 12:
                col_names = ["Personel Pronomen", "Konjunktiv II - Futur I"]
                karts = data[72:78]
            elif i == 13:
                col_names = ["Personel Pronomen", "Konjunktiv II - Futur II"]
                karts = data[78:84]
            elif i == 14:
                col_names = ["Personel Pronomen", "Imperativ"]
                karts = data[84:88]

            a = len(karts[0])
            datas = []

            if(a == 2):
                for i in karts:
                    datas.append([i[0], i[1]])
            elif(a == 3):            
                for i in karts:
                    datas.append([i[0], i[1] + " " + i[2]])
            elif(a == 4):
                for i in karts:
                    datas.append([i[0], i[1] + " " + i[2] + " " + i[3]])
            elif(a == 5):
                for i in karts:
                    datas.append([i[0], i[1] + " " + i[2] + " " + i[3] + " " + i[4]])
            
            # f.write(tabulate(datas, headers=col_names, tablefmt="fancy_grid"))
            # f.write("\n")

            # print(tabulate(datas, headers=col_names, tablefmt="fancy_grid"))
            # result += tabulate(datas, headers=col_names, tablefmt="fancy_grid")
            # result += "\n"
        return data
    except Exception as e:
        print(e)
        print(f"{istek} could not be found")

def Scraper(istek):
            data = []
            # Make a GET request to the website
            #istek = input("ein Verb eingeben: ")
            url = f"https://en.pons.com/verb-tables/german/{istek}"
            #headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all the tables with class "ft-single-table"
            tables = soup.find_all("div", class_="ft-single-table")
            # Loop through each table to extract the header and data
            for table in tables:
                for row in table.find("tbody").find_all("tr"):
                    columns = [col.text for col in row.find_all("td")]
                    data.append(columns)
            return data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    maker_results = []  # To store the results

    if request.method == "POST":
        word = request.form["word"]
        data = Scraper(word)  # Pass the input word to the Scraper function

        if data:
            maker_results = Maker(word, data)
              # Call Reverso function after getting Scraper data
            maker_results += Reverso(word)
        else:
            maker_results.append(f"Error: Could not retrieve data for '{word}'")

    return render_template("index.html", results=maker_results)

if __name__ == "__main__":
    app.run()

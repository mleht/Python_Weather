from urllib.request import urlopen
from urllib.parse import quote #ääkkösten avuksi quote
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import sqlite3
from datetime import datetime

def convertTuple(tup):  #tuplen purkamiseen stringiksi
    str =  ''.join(tup) 
    return str


def write_log(note):   
    time = datetime.now()
    log =  open("log.txt", "a")
    row = str(time) + " " + note
    log.write(row + "\r\n")
    log.close()

conn = sqlite3.connect('example.db')
c = conn.cursor()

print()
print("---------------------------------")
print("Welcome to Weather in Finland now!")
print("---------------------------------")
print()
print("This program shows you the temperature for the locations in the database.")
print("Do you want to save the new locations to the database?")
answer = input("If yes, please answer Y (any other answer is no): ")
if answer.upper()  == "Y":
    sql = "DROP TABLE IF EXISTS Paikkakunnat"
    c.execute(sql)
    sql2 = "CREATE TABLE Paikkakunnat(paikkakunta text)"
    c.execute(sql2)

    more = True
    print()
    print("Enter the location in Finland to save it in the database.")
    print("Simply pressing Enter (blank) will stop saving locations.")
    while more == True:
        user_input = input("Location: ")
        if user_input != "":
            c.execute("insert into Paikkakunnat(paikkakunta) values(?)", [user_input]) #estetään SQL-injection
            conn.commit() # tallennetaan muutokset
        else:
            more= False    

try:
    print()
    print("You have the following locations in your database:")

    sql = "SELECT paikkakunta FROM Paikkakunnat"
    for row in c.execute(sql):
        result = convertTuple(row) # tuple stringiksi
        print(result)       

    print()
    print("Do you want to try to get temperature information from the Finnish Meteorological Institute?")
    answer2 = input("If yes, please answer Y (any other answer is no): ")
    print()
    if answer2.upper()  == "Y":
        sql = "SELECT paikkakunta FROM Paikkakunnat"
        for row in c.execute(sql):
            location = convertTuple(row) # tuple stringiksi
            quote_page = f'https://www.ilmatieteenlaitos.fi/saa/'  + quote(f'{location}')
            response = requests.get(quote_page, timeout=10)
            if response.status_code == 200:
                page = urlopen(quote_page).read()
                soup = BeautifulSoup(page, 'html.parser') # Muuttujassa soup sivun html

                result2 = soup.find(class_="text-center fmi-bg-light temp")
                print(f"Temperature at {location} at the moment:")
                print(result2.text)
                write_log(f"Successful weather information:  {location}")
                print()
            else:
                print(f"Error with temperature at {location}") 
                write_log(f"Error: {location}")   
                print()

except:
    print("An error has occurred in the program. Are you sure you have locations in the database?")
finally:
    conn.close()
    print("The program ends.")







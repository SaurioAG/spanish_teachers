import requests
import pandas as pd
from bs4 import BeautifulSoup

def url_request(url: str):
    """
    This function will do a request to the given url and return a response object
    """
    request = requests.get(url)
    return request

def web_scraping(request):
    """
    This function receives a response object and parses the text on it to gather specific data
    Generates a CSV file with required data
    """
    TEACHER_DICT = {
        "id": "",
        "name": "",
        "verified": "",
        "nationality": "",
        "stars": "",
        "reviews": "",
        "price": "",
        "active_students": "",
        "clases": ""
    }
    teachers_list = []
    soup = BeautifulSoup(request.text, features = "html.parser")
    uls = soup.find_all("ul")
    for ul in uls:
        if ul.get("data-qa-group") != None:
            cards = ul
            break
    lis = cards.find_all("li")
    for li in lis:
        if li.get("data-qa-card-next-page") != None:
            section = li.find("section")
            TEACHER_DICT["id"] = section.get("data-qa-id")
            counter = 0
            for div in section.children:
                if counter == 1:
                    name = div.find_all("h4")[0].text
                    if len(div.find_all("span")) == 2:
                        verified = div.find_all("span")[0].get("aria-hidden")
                        nationality = div.find_all("span")[1].find("img").get("alt")
                    else:
                        print(div.find_all("span"))
                        verified = "false"
                        nationality = div.find_all("span")[0].find("img").get("alt")
                    TEACHER_DICT["name"] = name
                    TEACHER_DICT["verified"] = verified
                    TEACHER_DICT["nationality"] = nationality
                elif counter == 2:
                    stars = div.find_all("h4")[0].text
                    price = div.find_all("h4")[2].text
                    reviews = div.find_all("span")[0].text.split(" ")[0]
                    TEACHER_DICT["stars"] = stars
                    TEACHER_DICT["reviews"] = reviews
                    TEACHER_DICT["price"] = price
                elif counter == 4:
                    students = div.find_all("p")[1].text.split(" ")[0]
                    clases = div.find_all("p")[2].text.split(" ")[0]
                    TEACHER_DICT["active_students"] = students
                    TEACHER_DICT["clases"] = clases
                else:
                    pass
                counter += 1
            teachers_list.append(TEACHER_DICT.copy())
    dataframe = pd.DataFrame(teachers_list)
    print(dataframe)
    dataframe.to_csv("teachers_data.csv", index = False)

url = "https://preply.com/es/online/profesores--español?page=1" #have to loop thru pages from 1 to 721 in case of spanish teachers
request = url_request(url)
web_scraping(request)
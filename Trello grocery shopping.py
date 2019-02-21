import pandas as pd
import requests 
from io import StringIO


# constantes
reserve = "réserve"
courses = "courses"
trello_key = YOUR_KEY_HERE # replace with your trello keys


check_url="https://api.trello.com/1/boards/" + trello_key + "/checklists?checkItem_fields=state,name&key=9a4098751f7d038c893902cab5de1095&token=eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"
card_url="https://api.trello.com/1/boards/" + trello_key + "/cards?key=9a4098751f7d038c893902cab5de1095&token=eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"
list_url="https://api.trello.com/1/boards/" + trello_key + "/lists?key=9a4098751f7d038c893902cab5de1095&token=eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"

response_check = requests.request("GET", check_url)
response_card = requests.request("GET", card_url)
response_list = requests.request("GET", list_url)


cards = response_card.json()
lists =  response_list.json()
checks = response_check.json()

# reconstruire les lists
df_list = {}
for i in range(len(lists)):
    df_list[lists[i]["id"]] = lists[i]["name"]

# reconstruire les cards
df_card = {}
for i in range(len(cards)):
    df_card[cards[i]["id"]] = df_list[cards[i]["idList"]] + " // "  + cards[i]["name"] 


df_checks = []
df_checks_ok = []

for i in range(len(checks)):
    if (reserve not in df_card[checks[i]["idCard"]] and courses not in df_card[checks[i]["idCard"]]) :
        for j in range(len(checks[i]["checkItems"])):
            if checks[i]["checkItems"][j]["state"] == "incomplete" :
                df_checks.append(checks[i]["checkItems"][j]["name"]+ " ( => " + df_card[checks[i]["idCard"]]  + " )")
            else: 
                df_checks_ok.append(checks[i]["checkItems"][j]["name"]+ " ( => "  + df_card[checks[i]["idCard"]]  + " )"  )
    else: 
#  on en profite pour capter l'ID de la liste qui contient les courses à faire
        if "courses" in df_card[checks[i]["idCard"]]:
            card_course = checks[i]["idCard"]
            list_course = checks[i]["id"]


#print(df_checks, df_checks_ok)

# reset "courses "card content

url_del = "https://api.trello.com/1/checklists/" + list_course +"?key=9a4098751f7d038c893902cab5de1095&token=eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"
response = requests.request("DELETE", url_del)
#print(response.text)

url_create = "https://api.trello.com/1/checklists?key=9a4098751f7d038c893902cab5de1095&token=eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"
querystring = {"idCard":card_course}
response = requests.request("POST", url_create, params=querystring)
#print(response.text)
response = response.json()
list_course = response["id"]

# update "courses" card content

url_refr = "https://api.trello.com/1/checklists/" + list_course +"/checkItems"
querystring = {}

for i in range(len(df_checks)):
    querystring = {"name":df_checks[i],"pos":"bottom","key":"9a4098751f7d038c893902cab5de1095","token":"eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"}
    url = "https://api.trello.com/1/checklists/" + list_course + "/checkItems"
    response = requests.request("POST", url, params=querystring)
#    print(response.text)

for i in range(len(df_checks_ok)):
    querystring = {"name":df_checks[i],"pos":"bottom","checked":"true","key":"9a4098751f7d038c893902cab5de1095","token":"eef20901f16b8316f1f8644ba7fd2ff5bac11cb428ec24cf56eb2d7ee357cabd"}
    url = "https://api.trello.com/1/checklists/" + list_course + "/checkItems"
    response = requests.request("POST", url, params=querystring)
#    print(response.text)
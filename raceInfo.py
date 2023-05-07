import requests
from bs4 import BeautifulSoup as soup
import json


def get_input():
    year = int(input("Enter the year you want\n"))
    while year < 1950 or year > 2023:
        year = int(input(
            "No such year. Dates should be given between 1950 and 2022.\n"))
    return year


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_tbody(race_name, y):
    url = "https://www.formula1.com/en/results.html/"+str(y)+"/races/" + \
        race_name+"/race-result.html"
    doc = get_page(url)
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_race_input(races, y):
    print("These are the races of", y,
          "select the race you want by typing number of it.")

    for i in range(len(races)):
        print(i, "-", races[i][0].strip("-/1234567890"))
    ipt = input("Enter: ")
    while int(ipt) > len(races):
        ipt = input("Get your shit together and try again: ")
    # print("selected:", races[int(ipt)])
    if int(ipt) == 0:
        return "all"
    else:
        return races[int(ipt)][0]


def get_races(doc):
    main = doc.main
    article = main.article
    container = article.find(class_="resultsarchive-filter-container")
    rarchive1 = container.find(
        class_="resultsarchive-filter-wrap")
    rarchive2 = rarchive1.find_next(class_="resultsarchive-filter-wrap")
    rarchive3 = rarchive2.find_next(class_="resultsarchive-filter-wrap")
    lis = rarchive3.find_all("li", class_="resultsarchive-filter-item")
    race_links = []                                 # bunu dict ile yapmaya calis
    for li in lis:
        race_links.append([item["data-value"]
                           for item in li.find_all() if "data-value" in item.attrs])
    return race_links


def get_driver_name(tbody):
    list_of_names = []
    tds = tbody.find_all("td", class_="dark bold")
    for td in tds:
        names = td.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        if not names:
            continue
        else:
            name = names[0].string + " " + names[1].string
            list_of_names.append(name)
    return list_of_names


def get_team_name(tbody):
    list_of_teams = []
    tds = tbody.find_all("td", class_="semi-bold uppercase hide-for-tablet")
    for td in tds:
        list_of_teams.append(td.text)
    return list_of_teams


def get_laps(tbody):
    list_of_completed_laps = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        list_of_completed_laps.append(td.text)
    return list_of_completed_laps


def get_times(tbody):
    list_of_times = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        time = td.find_next(class_="dark bold")
        list_of_times.append(time.text)
    return list_of_times


def get_points(tbody):
    list_of_points = []
    tds = tbody.find_all(lambda tag: tag.name ==
                         "td" and tag["class"] == ["bold"])
    for td in tds:
        list_of_points.append(td.text)
    return list_of_points


drivers_dict = {}


def update_dict(drivers):
    for i in range(len(drivers)):
        if drivers[i] not in drivers_dict:
            drivers_dict[drivers[i]] = []
            drivers_dict[drivers[i]].append(i+1)
        else:
            drivers_dict[drivers[i]].append(i+1)


def print_dictionary(my_dict):
    for key, value in my_dict.items():
        print(f'{key}: {value}')


def save(filename):
    # Open the file in write mode and save the contents of the global dictionary to it
    with open(filename, 'w') as json_file:
        json.dump(drivers_dict, json_file)


def main():
    open("raceInfo.json", "w").flush()
    year = get_input()
    url = "https://www.formula1.com/en/results.html/"+str(year)+"/races.html"
    doc = get_page(url)
    race_links = get_races(doc)
    for index in range(1, len(race_links)):

        race_name = race_links[index][0]
        tbody = get_tbody(race_name, year)
        name = get_driver_name(tbody)
        #team = get_team_name(tbody)
        #completed_laps = get_laps(tbody)
        #times = get_times(tbody)
        #points = get_points(tbody)
        #quali = get_quali_res(tbody)
        update_dict(name)
        save("raceInfo.json",)
    print("done")
    print_dictionary(drivers_dict)


main()

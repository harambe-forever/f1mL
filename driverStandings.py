import requests
from bs4 import BeautifulSoup as soup
import time


def strip_down_to_tbody(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    #
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    #
    return tbody


def get_drivers(tbody):
    drivers_this_season = []
    tds_for_names = tbody.find_all("a", class_="dark bold ArchiveLink")
    for td_for_names in tds_for_names:
        names = td_for_names.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        name = names[0].text + " " + names[1].text
        drivers_this_season.append(name)
        # print("Name:", name)
    return drivers_this_season


def get_points(tbody):
    points_this_season = []
    tds_for_points = tbody.find_all("td", class_="dark bold")
    for td_for_points in tds_for_points:
        point = td_for_points.string
        points_this_season.append(point)
        # print("PTS:", point)
    return points_this_season


def get_teams(tbody):
    teams_this_season = []
    tds_for_teams = tbody.find_all(
        "a", class_="grey semi-bold uppercase ArchiveLink")
    for td_for_teams in tds_for_teams:
        team = td_for_teams.string
        teams_this_season.append(team)
        # print("Team:", team)
    return teams_this_season


def get_input():
    year = int(input("Enter the year you want\n"))
    while year < 1950 or year > 2023:
        year = int(input(
            "No such year. Dates should be given between 1950 and 2022.\n"))
    return year


def init():
    year = get_input()
    url = "https://www.formula1.com/en/results.html/" + \
        str(year)+"/drivers.html"
    tbody = strip_down_to_tbody(url)
    drivers = get_drivers(tbody)
    teams = get_teams(tbody)
    points = get_points(tbody)
    return drivers, teams, points


def save(path):
    driverStandings = []
    drivers, teams, points = init()
    for i in range(len(drivers)):
        driver = drivers[i]
        team = teams[i]
        point = points[i]
        #print("{0},{1},{2}".format(driver, team, point))
        driverStandings.append("{0},{1},{2}".format(driver, team, point))
    with open(path, "a", encoding="utf-8") as f:
        for line in driverStandings:
            f.write(line + "\n")


def main():
    open("driverStandings.csv", "w").flush()
    save("driverStandings.csv")
    print("done;D")


main()

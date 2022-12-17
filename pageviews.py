import pandas as pd
from datetime import date, timedelta, datetime
import requests
import json


def get_page_views_new(
        raw_url = "https://en.wikipedia.org/wiki/Nigeria",
        access="all-access",
        agent="all-agents",
        granularity="daily",
        start_date= date(2016,1,1),
        end_date=date.today()):
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    base_url = "https://wikimedia.org/api/rest_v1/metrics/"
    lang = raw_url[8:10]
    project = lang+".wikipedia.org"
    sdate = date.strftime(start_date, '%Y%m%d')
    edate = date.strftime(end_date, '%Y%m%d')
    article = raw_url.lstrip("https://" + lang + ".wikipedia.org/wiki/")
    url = base_url +"pageviews/per-article/{}/{}/{}/{}/{}/{}/{}".format(project, access, agent, article, granularity, sdate, edate)
    response = requests.get(url, headers=headers)
    data = response.json()
    df = pd.json_normalize(data["items"])
    df["date"] = df["timestamp"].apply(lambda x: datetime.strptime(x, '%Y%m%d%H').strftime('%Y-%m-%d'))
    df = df.drop(columns=["project", "granularity", "access", "agent", "timestamp"])
    metadata = {"project": project, "granularity": granularity, "access": access, "agent": agent}
    return df, metadata


def get_page_views_old(raw_url="https://en.wikipedia.org/wiki/Nigeria"):
    lang = raw_url[8:10]
    article = raw_url.lstrip("https://" + lang + ".wikipedia.org/wiki/")
    base_url_old = "http://petermeissner.de:8880/article/exact/{}/{}"
    url= base_url_old.format(lang, article)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return print(err)
    data = response.json()
    df = pd.json_normalize(data["data"])
    df = df[df["year"] != 2007]
    df["page_view_count_list"] = df["page_view_count"].apply(lambda x: [eval(i) for i in x.split(",")])
    df = df.sort_values(by= ["year"])
    df = df.explode("page_view_count_list")
    date_range = pd.date_range("2008-01-01", "2015-12-31", freq="D")
    df["date"] = list(date_range)
    df["views"] = df["page_view_count_list"].astype(int)
    df = df.rename(columns={"page_name": "article"})
    df = df.drop(columns=["page_view_count", "page_view_count_list", "year"])
    metadata = {"project": lang+".wikipedia.org", "granularity": "daily", "access": "all-access", "agent": "all-agents"}
    return df, metadata


def get_page_views_from_url_list(liste, time_period = "new"):
    liste_df = []
    for url in liste:
        if time_period == "new":
            df_temp, metadata = get_page_views_new(url)
        elif time_period == "old":
            df_temp, metadata = get_page_views_old(url)
        liste_df.append(df_temp)
    return pd.concat(liste_df)




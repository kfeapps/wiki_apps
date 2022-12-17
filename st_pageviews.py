import pandas as pd
import streamlit as st
from pageviews import get_page_views_old, get_page_views_new, get_page_views_from_url_list
from aux_viz import plot_time_series
import plotly.express as px


st.set_page_config(
	layout="wide"
)

path_admin1_wiki_links = "data/admin1_africa_en_fr_ar_de_es_it.parquet.parquet"

dict_wikis = {
	"en": "English Wikipedia",
	"fr": "French Wikipedia",
	"ar": "Arabic Wikipedia",
	"de": "German Wikipedia",
	"es": "Spanish Wikipedia",
	"it": "Italian Wikipedia"}


@st.experimental_memo
def load_admin1_wiki_links(path):
	return pd.read_parquet(path)


@st.experimental_memo
def get_sorted_country_list(df):
	return sorted(df["NAME_COUNTRY"].unique().tolist())


def filter_by_country(df, selected_countries):
	return df[df["NAME_COUNTRY"].isin([selected_countries])]


def get_sorted_admin1_list(df):
	return sorted(df["NAME_ADMIN1"].unique().tolist())


@st.experimental_memo
def get_dict_lang_links(df_temp, lang):
	return df_temp.set_index("NAME_ADMIN1").to_dict()["URL_ARTICLE_"+lang.upper()]


def get_url_from_name_list(liste_names, dict_urls):
	return [dict_urls[name] for name in liste_names]


@st.experimental_memo
def filter_by_lang(df_temp, lang):
	return df_temp.dropna(subset=["URL_ARTICLE_"+lang.upper()])


df_admin1 = load_admin1_wiki_links(path_admin1_wiki_links)
country_list = get_sorted_country_list(df_admin1)

st.header("Wikipedia Pageviews for ADMIN1-regions in Africa")

col_time_period, col_lang, col_admin0, col_admin1, col_freq, col_chart_option = st.columns(6)
with col_time_period:
	sel_time_period = st.selectbox(
		"Select a time period",
		options= ["old", "new"],
		index = 1,
		format_func= lambda x: {"old": "2008 to 2015", "new": "2016 to now"}[x]
	)
with col_lang:
	sel_lang = st.selectbox(
		"Select language",
		options = ["en", "fr", "ar", "de", "es", "it"],
		format_func= lambda x: dict_wikis[x],
		index = 0
	)
	dict_lang = get_dict_lang_links(df_admin1, sel_lang)
with col_freq:
	sel_agg_period = st.selectbox(
		"Select aggregation period",
		options = ["D", "W", "M", "Q", "Y"],
		format_func=lambda x: {"D": "Day", "W": "Week", "M": "Month", "Q": "Quarter", "Y": "Year"}[x],
		index=0
	)
with col_admin0:
	sel_countries = st.selectbox(
		"Select country",
		options=country_list,
		index=0
	)
with col_admin1:
	sel_admin1 = st.multiselect(
		"Select ADMIN1-region",
		options=get_sorted_admin1_list(filter_by_country(filter_by_lang(df_admin1, sel_lang), sel_countries))
		)
with col_chart_option:
	sel_chart_option = st.selectbox(
		"Select a chart option",
		options = ["agg", "stacked", "compare"],
		format_func= lambda  x: {"agg": "Aggregation - Line Chart", "stacked": "Stacked - Area Chart", "compare": "Comparison - Line Chart" }[x],
		index=0
	)
if sel_admin1:
	df_site_views= get_page_views_from_url_list(get_url_from_name_list(sel_admin1,dict_lang),sel_time_period)
	st.plotly_chart(plot_time_series(df_site_views, sel_agg_period, sel_chart_option), use_container_width=True)
	#st.table(df_site_views)
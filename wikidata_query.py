# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint_url = "https://query.wikidata.org/sparql"

query_1 = """SELECT DISTINCT ?region ?regionLabel ?countryLabel ?countryCode ?ISO_CODE ?HASC ?sl ?article_en ?article_fr  ?article_ar
WHERE {
  ?country wdt:P30 wd:Q15 .
  ?region wdt:P17 ?country .
  ?region wdt:P31/wdt:P279* wd:Q10864048 . 
  ?country wdt:P298 ?countryCode .
  OPTIONAL  {
  ?region wikibase:sitelinks ?sl .}
  OPTIONAL  {
  ?region ^schema:about ?article_en . 
  ?article_en schema:isPartOf <https://en.wikipedia.org/>.}
  OPTIONAL  {
  ?region ^schema:about ?article_ar . 
  ?article_ar schema:isPartOf <https://ar.wikipedia.org/>.}
  OPTIONAL  {
  ?region ^schema:about ?article_fr . 
  ?article_fr schema:isPartOf <https://fr.wikipedia.org/>.
  }
  OPTIONAL { ?region wdt:P300 ?ISO_CODE.}
  OPTIONAL { ?region wdt:P8119 ?HASC. }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}"""

query_2 = """SELECT DISTINCT ?region ?regionLabel ?countryLabel ?countryCode ?ISO_CODE ?HASC ?sl ?article_de ?article_es ?article_it
WHERE {
  ?country wdt:P30 wd:Q15 .
  ?region wdt:P17 ?country .
  ?region wdt:P31/wdt:P279* wd:Q10864048 . 
  ?country wdt:P298 ?countryCode .
  OPTIONAL  {
  ?region wikibase:sitelinks ?sl .}
  OPTIONAL  {
  ?region ^schema:about ?article_de . 
  ?article_de schema:isPartOf <https://de.wikipedia.org/>.}
  OPTIONAL  {
  ?region ^schema:about ?article_es . 
  ?article_es schema:isPartOf <https://es.wikipedia.org/>.}
  OPTIONAL  {
  ?region ^schema:about ?article_it . 
  ?article_it schema:isPartOf <https://it.wikipedia.org/>.
  }
  OPTIONAL { ?region wdt:P300 ?ISO_CODE.}
  OPTIONAL { ?region wdt:P8119 ?HASC. }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results_1 = get_results(endpoint_url, query_1)
results_2 = get_results(endpoint_url, query_2)



dict_codes_1 = {"countryCode.value": "ISO3_ADMIN0",
                        "region.value": "WDID_ADMIN1",
                        "ISO_CODE.value": "ISO2-2_ADMIN1",
                        "regionLabel.value": "NAME_ADMIN1",
                        "countryLabel.value": "NAME_COUNTRY",
                        "HASC.value": "CODE_HASC",
                        "sl.value": "sitelinks",
                        "article_en.value": "URL_ARTICLE_EN",
                        "article_fr.value": "URL_ARTICLE_FR",
                        "article_ar.value": "URL_ARTICLE_AR",
              }


dict_codes_2 = {"countryCode.value": "ISO3_ADMIN0",
                        "region.value": "WDID_ADMIN1",
                        "ISO_CODE.value": "ISO2-2_ADMIN1",
                        "regionLabel.value": "NAME_ADMIN1",
                        "countryLabel.value": "NAME_COUNTRY",
                        "HASC.value": "CODE_HASC",
                        "sl.value": "sitelinks",
                        "article_de.value": "URL_ARTICLE_DE",
                        "article_es.value": "URL_ARTICLE_ES",
                        "article_it.value": "URL_ARTICLE_IT",
              }


df = pd.json_normalize(results_1["results"]["bindings"])
df = df.rename(columns=dict_codes_2)
df = df[list(dict_codes_2.values())]
df = df.rename(columns=dict_codes_2)
df = df[list(dict_codes_2.values())]


df_2 = pd.json_normalize(results_2["results"]["bindings"])
df_2 = df_2.rename(columns=dict_codes_2)
df_2 = df_2[list(dict_codes_2.values())]
df_2 = df_2.rename(columns=dict_codes_2)
df_2 = df_2[list(dict_codes_2.values())]

df_3 = df_2[["WDID_ADMIN1", "URL_ARTICLE_DE", "URL_ARTICLE_ES", "URL_ARTICLE_IT"]]
A = pd.merge(df, df_3, how="right", on=["WDID_ADMIN1"])
A.to_parquet("data/admin1_africa_en_fr_ar_de_es_it.parquet")

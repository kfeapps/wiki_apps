# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT DISTINCT ?region ?regionLabel ?countryLabel ?countryCode ?ISO_CODE ?HASC ?sl ?article_en ?article_fr  ?article_ar
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


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

df = pd.json_normalize(results["results"]["bindings"])

dict_codes = {"countryCode.value": "ISO3_ADMIN0",
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

df = df.rename(columns=dict_codes)

df = df[list(dict_codes.values())]

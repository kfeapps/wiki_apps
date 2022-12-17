query_1 = """select ?region ?regionLabel ?ISO_CODE ?HASC
{ VALUES ?country {wd:Q974} # get the top level regions of the country 
  ?region wdt:P17 ?country . 
  ?region wdt:P31/wdt:P279* wd:Q10864048 . 
  ?region wdt:P300 ?ISO_CODE.
  OPTIONAL { ?region wdt:P8119 ?HASC. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }"""


query_2 = """SELECT DISTINCT ?region ?regionLabel ?countryLabel ?countryCode ?ISO_CODE ?HASC
WHERE {
  ?region wdt:P31/wdt:P279* wd:Q10864048 . 
  ?region wdt:P17 ?country .
  ?country wdt:P30 wd:Q15 .
  ?country wdt:P298 ?countryCode .
  OPTIONAL { ?region wdt:P300 ?ISO_CODE.}
  OPTIONAL { ?region wdt:P8119 ?HASC. }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}
"""

query_3 = """SELECT ?lang (COUNT(DISTINCT ?article) AS ?count) WHERE {
  hint:Query hint:optimizer "None".
  ?item wdt:P1367 ?yp_id .
  ?article schema:about ?item . # find articles about things with a BBC 'Your paintings' artist identifier
  ?article schema:isPartOf / wikibase:wikiGroup "wikipedia" . # only Wikipedias articles
  hint:Prior hint:gearing "forward" .
  # This hint says to search the property chain above from left to right ("forward"),
  # i.e. it is checked if each previously found value for ?article is linked to a Wikipedia.
  # The default ("reverse") would be to search it from right to left, i.e. find all Wikipedia
  # articles first, and then select the intersection with the previously found values of ?article.
  ?article schema:inLanguage ?lang .
} GROUP BY ?lang
ORDER BY DESC (?count)"""
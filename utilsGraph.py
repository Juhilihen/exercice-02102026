"""Helpers pour lire le graphe RDF (rdflib) et faire de la NER (spaCy)."""

import os
from urllib.parse import quote

import spacy
from rdflib import Graph
from rdflib.namespace import SKOS


# ADDING PLURITAL AS A NAMESPACE
PLURITAL = "https://plurital.org/ns/model#"


_nlp = None

def getNlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("fr_core_news_md")
    return _nlp


""" Loading graphs in our folder associated with an image to display in our Web Service"""
def loadGraphs(graphFolder, graphFile=None):
    graph = Graph()
    if graphFile and graphFile.endswith(".rdf"):
        path = os.path.join(graphFolder, os.path.basename(graphFile))
        if os.path.isfile(path):
            graph.parse(path, format="xml")
    else:
        for fileName in sorted(os.listdir(graphFolder)):
            if fileName.endswith(".rdf"):
                graph.parse(os.path.join(graphFolder, fileName), format="xml")
    return graph

"""  Displaying coordinates and the chosen properties for each resource"""
def listResources(graphFolder, graphFile=None):
    graph = loadGraphs(graphFolder, graphFile)
    query = f"""
        PREFIX skos: <{SKOS}>
        PREFIX plurital: <{PLURITAL}>
        SELECT ?resource ?label ?definition ?image ?hl ?hr ?lf ?lr WHERE {{
            ?resource a skos:Concept .
            ?resource skos:prefLabel ?label .
            OPTIONAL {{ ?resource skos:definition ?definition . }}
            OPTIONAL {{ ?resource plurital:image ?image . }}
            OPTIONAL {{ ?resource plurital:hl ?hl . }}
            OPTIONAL {{ ?resource plurital:hr ?hr . }}
            OPTIONAL {{ ?resource plurital:lf ?lf . }}
            OPTIONAL {{ ?resource plurital:lr ?lr . }}
        }}
    """
    resources = []
    for row in graph.query(query):
        resources.append({
            "id": str(row.resource).split("/")[-1],
            "label": str(row.label),
            "definition": str(row.definition) if row.definition else "",
            "image": str(row.image) if row.image else "",
            "hl": str(row.hl) if row.hl else None,
            "hr": str(row.hr) if row.hr else None,
            "lf": str(row.lf) if row.lf else None,
            "lr": str(row.lr) if row.lr else None,
        })
    return resources

"""Each ConcepstScheme being parsed"""
def listConceptSchemes(graphFolder, graphFile=None):
    graph = loadGraphs(graphFolder, graphFile)
    query = f"""
        PREFIX skos: <{SKOS}>
        SELECT ?scheme ?predicate ?value WHERE {{
            ?scheme a skos:ConceptScheme .
            ?scheme ?predicate ?value .
        }}
    """
    schemes = {}
    for row in graph.query(query):
        schemeId = str(row.scheme)
        scheme = schemes.setdefault(schemeId, {
            "id": schemeId.split("/")[-1],
            "properties": [],
        })
        scheme["properties"].append({
            "predicate": str(row.predicate),
            "value": str(row.value),
        })
    return list(schemes.values())

""" Spacy Demo function """
def extractEntities(text):
    doc = getNlp()(text)
    return [
        {
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
            "suggested_uri": quote(ent.text, safe=""),
        }
        for ent in doc.ents
    ]

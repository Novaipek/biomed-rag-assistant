import requests
import xml.etree.ElementTree as ET
from biomed_rag.data.models import Article 

class PubMedClient:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


    def search(self, query):
        response = requests.get(self.base_url+"esearch.fcgi",
                               params={
                                      "db": "pubmed",
                                      "term": query,
                                      "retmode": "json",
                                      "retmax": 100
                               })
        data = response.json()
        return data["esearchresult"]["idlist"]
                               
    def fetch_articles(self, pmid_list):
        response = requests.get(self.base_url+"efetch.fcgi",
                               params={
                                        "db":"pubmed",
                                        'retmode':'xml',
                                        'id': ','.join(pmid_list)

                                   })
        return response.text
    
    def parse_article(self, xml_data):
        root = ET.fromstring(xml_data)
        pmid = root.find(".//PMID").text
        title = root.find('.//ArticleTitle').text
        journal = root.find('.//Journal/Title').text
        published_year = int(root.find('.//PubDate/Year').text)
        abstract = root.find ('.//AbstractText')
        abstract = abstract.text if abstract is not None else None
        authors = []
        for author in root.findall('.//Author'):
            last_name = author.find('LastName')
            first_name = author.find('ForeName')
            if last_name is not None and first_name is not None:
                authors.append(f"{first_name.text} {last_name.text}")
        doi = root.find('.//ELocationID[@IdType="doi"]') 
        doi = doi.text if doi is not None else None
        return Article(
            pmid=pmid,
            title=title,
            journal=journal,
            published_year=published_year,
            abstract=abstract,
            authors=authors,
            doi=doi
        )
    def parse_articles(self, xml_data):
        root = ET.fromstring(xml_data)
        articles = []
        for article in root.findall('.//PubmedArticle'):
            articles.append(self.parse_article(ET.tostring(article,encoding='unicode')))
        return articles


import sqlite3
from biomed_rag.data.models import Article

class Database:
    def __init__(self,db_path:str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    def create_table(self):
        """articles table"""
        sql = '''
            CREATE TABLE IF NOT EXISTS articles(
            pmid TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            abstract TEXT,
            authors TEXT,
            journal TEXT NOT NULL,
            published_year INTEGER NOT NULL,
            doi TEXT
            )'''
        self.conn.execute(sql)
        self.conn.commit()

    def save_article(self,article:Article):
            
        sql = """
            INSERT OR IGNORE INTO articles
            (pmid, title, abstract, authors, journal, published_year, doi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        values = (
            article.pmid,
            article.title,
            article.abstract,
            '|'.join(article.authors),
            article.journal,
            article.published_year,
            article.doi
        )

        self.conn.execute(sql,values)
        self.conn.commit()
        
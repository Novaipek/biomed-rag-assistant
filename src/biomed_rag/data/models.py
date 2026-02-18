from pydantic import BaseModel
class Article(BaseModel):
    pmid: str
    authors: list[str] = []
    title: str
    abstract: str | None = None
    journal: str
    published_year: int
    doi: str | None = None
class SearchResult(BaseModel):
    query: str
    articles: list[Article] = []
    total_count : int = 0

    
    

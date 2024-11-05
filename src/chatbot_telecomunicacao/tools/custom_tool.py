from crewai_tools import BaseTool
from crewai_tools import PDFSearchTool, SerperDevTool
    
# Especificação de sites para raspagem
class WebSite_Search(BaseTool):
    name: str = "Search on the web"
    description: str = (
        "Use this to search on the web"
    )

    def _run(self):
        search_tool = SerperDevTool(
            website_url=[ 
                "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/banda-larga",
                "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-movel",
                "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-fixa",
                "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/tv-por-assinatura"
            ]
        )
        return search_tool

# Ferramenta para RAG em arquivos PDF. Específica para fazer buscas e extrair partes relevantes em arquivos PDF. 
class Pdf_Search(BaseTool):
    name: str = "Get the PDF from normas/"
    description: str = (
        "Use this for RAG in PDFs"
    )

    def _run(self):
        pdf_search = PDFSearchTool(pdf="normas/335492.pdf")
        pdf_search1 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 426, de 9 de dezembro de 2005.pdf")
        pdf_search2 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 477, de 7 de agosto de 2007.pdf")
        pdf_search3 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 488, de 3 de dezembro de 2007.pdf")
        pdf_search4 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 581, de 26 de março de 2012.pdf")
        pdf_search5 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 632, de 7 de março de 2014.pdf")
        pdf_search6 = PDFSearchTool(pdf="normas/oficio_12273325.pdf")
        
        return pdf_search, pdf_search1, pdf_search2, pdf_search3, pdf_search4, pdf_search5, pdf_search6



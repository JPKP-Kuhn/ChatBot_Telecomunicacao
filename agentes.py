import os
from crewai_tools import tool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool,PDFSearchTool, TXTSearchTool
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from ia import get_openai_api_key, get_serper_api_key

openai_api_key = get_openai_api_key()
serper_api_key = get_serper_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

gpt4o_mini_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

# Ferramenta para busca no google
search_tool = SerperDevTool()

# Ferramenta para raspagem de sites
scrape_tool = ScrapeWebsiteTool()

# Ferramenta para raspagem de arquivo txt, para as respostas exemplo.
texto_search = TXTSearchTool("normas/resposta_exemplar.txt")

# Especificação de apenas um site para raspagem
docs_scrape_tool = ScrapeWebsiteTool(
    website_url=[
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/banda-larga",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-movel",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-fixa",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/tv-por-assinatura",
        "https://www.gov.br/anatel/pt-br/consumidor/perguntas-frequentes"
    ]
)
docs_search_tool = WebsiteSearchTool(website_url="https://www.gov.br/anatel/pt-br/consumidor/perguntas-frequentes")

# Ferramenta para RAG em arquivos PDF. Específica para fazer buscas e extrair partes relevantes em arquivos PDF. 

# Normas da Anatel
pdf_search = PDFSearchTool(pdf="normas/Anatel - Manual Explicativo.pdf")
pdf_search1 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 426, de 9 de dezembro de 2005.pdf")
pdf_search2 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 477, de 7 de agosto de 2007.pdf")
pdf_search3 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 488, de 3 de dezembro de 2007.pdf")
pdf_search4 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 581, de 26 de março de 2012.pdf")
pdf_search5 = PDFSearchTool(pdf="normas/Anatel - Resolução nº 632, de 7 de março de 2014.pdf")

# Datasheets
datasheet_search = PDFSearchTool(pdf="datasheets/Datasheet_Impacta_16_Impacta_40_Impacta_68i_0.pdf")
datasheet_search1 = PDFSearchTool(pdf="datasheets/Datasheet-AE-1028-01.20.pdf")
datasheet_search2 = PDFSearchTool(pdf="datasheets/PABX_-_Configuracao-2.19-v.pdf")
#Definição dos 4 agentes:
identificador = Agent(
    role="Identificador de Problemas",
    goal="Receber a dúvida do cliente e identificar de qual área é o seguinte problema: {problema}",
    backstory="Você está trabalhando na identificação de um problema de telecomunicações"
              "sobre o problema: {problema}."
              "Você coleta informações atualizadas através de sites e arquivos que ajudam a "
              "identificar a área do problema "
              "e indica qual é o agente especializado no problema, caracterizando-o em jurídico, se for mais relacionado a alguma norma,"
              "ou técnico, se está relacionado com o uso de algum equipamento. "
              "As únicas duas áreas de problemas principais são Jurídico e Técnico "
              "Seu trabalho é a base para que o "
              "agente seguinte escreva possíveis soluções para o problema."
              "O próximo agente pode ser o Solucionador de problemas da área Jurídica ou o Solucionador de problemas da área Técnica ",
    verbose=True,
    tools=[search_tool, scrape_tool, docs_scrape_tool, docs_search_tool, texto_search],
    allow_delegation=False,
    llm=gpt4o_mini_llm
)

juridico = Agent(
    role="Solucionador de problemas da área Jurídica",
    goal="Definir uma solução, com base nas leis da Anatel, nas perguntas frequentes da Anatel e no arquivo txt resposta_exemplar, para o cliente a fim de resolver seu questionamento: {problema}",
    backstory="Você é um solucionador que recebe um problema de um cliente. "
              "Seu objetivo é dar soluções jurídicas para o problema do cliente, baseando-se nas normas da Anatel."
              "Você também fornece insights objetivos e imparciais "
              "e os apoia com as informações "
              "baseadas nas leis da Anatel e regulamentações da Anatel. "
              "Após análise concluída você escreve um pequeno texto, semelhante às respostas da Anatel para perguntas frequentes, aconselhando o cliente para a solução do seu problema."
              "Envie esse texto resumido para o Supervisor de artigos"
              "Caso o problema não tenha nenhuma relação com telecomunicações ou com Anatel, retorne apenas um comentário dizendo que você não é capaz de resolver seu problema.",
    verbose=True,
    tools=[pdf_search, pdf_search1, pdf_search2, pdf_search3, pdf_search4, pdf_search5, texto_search, docs_search_tool],
    allow_delegation=False,
    llm=gpt4o_mini_llm
)


tecnico = Agent(
    role="Solucionador de problemas da área Técnica",
    goal="Definir uma solução, com base em datasheets sobre o produto ou equipamento definidos pelo cliente para solução do problema: {problema}",
    backstory="Você é um solucionador que recebe um problema de um cliente de telecomunicações, podendo este ser um técnico ou um engenheiro. "
              "Seu objetivo é dar soluções técnicas para o problema do cliente."
              "Você também fornece insights objetivos e imparciais "
              "e os apoia com as informações "
              "fornecidas pelos datasheets. "
              "Após análise concluída você escreve um pequeno texto, semelhante às respostas da Anatel para perguntas frequentes, aconselhando o cliente para a solução do seu problema."
              "Envie esse texto resumido para o Supervisor de artigos"
              "Caso o problema não tenha nenhuma relação com telecomunicações ou com Anatel, retorne apenas um comentário dizendo que você não é capaz de resolver seu problema.",
    verbose=True,
    tools=[pdf_search, datasheet_search, datasheet_search1, datasheet_search2, texto_search, docs_search_tool],
    allow_delegation=False,
    llm=gpt4o_mini_llm
)

supervisor = Agent(
    role="Supervisor de artigos",
    goal="Analisar e corrigir possíveis erros cometidos pelo agente jurídico e pelo técnico para solucionar o seguinte problema: {problema}",
    backstory="Você é um supervisor de artigos que recebe um texto com soluções para o problema: {problema}."  
              "Seu objetivo é supervisar os textos produzidos pelos agentes jurídicos e técnicos, corrigindo erros jurídicos, técnicos e gramaticais da lígua portuguesa e também que ela seja conciso na resposta para o cliente, baseando nas respostas da Anatel para as perguntas frequentes ."
              "Você deve verificar se as soluções são coerentes com as leis da Anatel, com os datasheets utilizados para consulta e usar o modelo resposta_exemplar.txt."
              "Caso o problema não seja da área da Telecomunicações, apague o texto do solucionador de problemas e escreva que o problema está fora do escopo"
              "Por fim, retorne o documento corrigido, resumido e com no máximo 800 caracteres e com as referências da pesquisa ao final.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool, docs_scrape_tool, docs_search_tool, pdf_search, pdf_search1, pdf_search2, pdf_search3, pdf_search4, pdf_search5, texto_search],
    llm=gpt4o_mini_llm
)

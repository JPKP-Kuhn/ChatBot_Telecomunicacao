import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import tool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool, PDFSearchTool
from chatbot_telecomunicacao.tools.custom_tool import *
from langchain_openai import ChatOpenAI

pdf_search = Pdf_Search()

# Ferramenta para busca no google
search_tool = SerperDevTool()

# Ferramenta para raspagem de sites
scrape_tool = ScrapeWebsiteTool()

# Especificação de sites para raspagem
docs_scrape_tool = WebSite_Search()

@CrewBase
class ChatbotTelecomunicacaoCrew():
	"""ChatbotTelecomunicacao crew"""

	@agent
	def identificador(self) -> Agent:
		return Agent(
			config=self.agents_config['identificador'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
			#llm=gpt4o_mini_llm
		)

	@agent
	def juridico(self) -> Agent:
		return Agent(
			config=self.agents_config['juridico'],
			verbose=True,
   			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
		)
  
	@agent
	def tecnico(self) -> Agent:
		return Agent(
			config=self.agents_config['tecnico'],
			verbose=True,
			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
		)
  
	@agent
	def supervisor(self) -> Agent:
		return Agent(
			config=self.agents_config['supervisor'],
			verbose=True,
			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
		)

	@task
	def identificacao(self) -> Task:
		return Task(
			config=self.tasks_config['identificacao'],
   			expected_output="Passar o problema para o agente responsável pela área ",
		)

	@task
	def solucao_juridica(self) -> Task:
		return Task(
			config=self.tasks_config['solucao_juridica'],
			expected_output="Caso o problema seja de sua área, envie esse documento para o Supervisor de artigos",
			output_file='report.md'
		)
  
	@task
	def solucao_tecnica(self) -> Task:
		return Task(
			config=self.tasks_config['solucao_tecnica'],
			expected_output="Caso o problema seja de sua área, envie esse documento para o Supervisor de artigos",
			output_file='report.md'
		)
  
	@task
	def supervisar(self) -> Task:
		return Task(
			config=self.tasks_config['supervisar'],
   			expected_output="Um documento com soluções bem escrito, em português do Brasil, "
            "com cada seção contendo 3 ou 4 parágrafos. Ao final, as referências utilizadas no documento.",
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ChatbotTelecomunicacao crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

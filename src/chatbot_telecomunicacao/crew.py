import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import tool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool, PDFSearchTool
from chatbot_telecomunicacao.tools.custom_tool import *
from langchain_openai import ChatOpenAI

# Uncomment the following line to use an example of a custom tool
# from chatbot_telecomunicacao.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

openai_api_key = Get_API_Key("../.env/OPENAI_API_KEY")
serper_api_key = Get_API_Key("../.env/SERPER_API_KEY")
pdf_search = Pdf_Search()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

gpt4o_mini_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

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
			llm=gpt4o_mini_llm
		)

	@agent
	def juridico(self) -> Agent:
		return Agent(
			config=self.agents_config['juridico'],
			verbose=True,
   			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
			llm=gpt4o_mini_llm
		)
  
	@agent
	def tecnico(self) -> Agent:
		return Agent(
			config=self.agents_config['tecnico'],
			verbose=True,
			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
			llm=gpt4o_mini_llm
		)
  
	@agent
	def supervisor(self) -> Agent:
		return Agent(
			config=self.agents_config['supervisor'],
			verbose=True,
			tools=[search_tool, scrape_tool, docs_scrape_tool, pdf_search],
			allow_delegation=False,
			llm=gpt4o_mini_llm
		)

	@task
	def identificacao(self) -> Task:
		return Task(
			config=self.tasks_config['identificacao'],
		)

	@task
	def solucao_juridica(self) -> Task:
		return Task(
			config=self.tasks_config['solucao_juridica'],
			output_file='report.md'
		)
  
	@task
	def solucao_tecnica(self) -> Task:
		return Task(
			config=self.tasks_config['solucao_tecnica'],
			output_file='report.md'
		)
  
	@task
	def supervisar(self) -> Task:
		return Task(
			config=self.tasks_config['supervisar'],
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
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from chatbot_telecomunicacao.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class ChatbotTelecomunicacaoCrew():
	"""ChatbotTelecomunicacao crew"""

	@agent
	def identificador(self) -> Agent:
		return Agent(
			config=self.agents_config['identificador'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def juridico(self) -> Agent:
		return Agent(
			config=self.agents_config['juridico'],
			verbose=True
		)
  
	@agent
	def tecnico(self) -> Agent:
		return Agent(
			config=self.agents_config['tecnico'],
			verbose=True
		)
  
	@agent
	def supervisor(self) -> Agent:
		return Agent(
			config=self.agents_config['supervisor'],
			verbose=True
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
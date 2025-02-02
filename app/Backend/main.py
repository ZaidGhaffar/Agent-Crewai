from crewai import Agent,LLM,Process,Crew,Task
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Please Enter GEMINI API KEY")
    
    
    
class Sdlc_Pipeline:
    def __init__(self):
        self.crew = None
        self.agents = {}
        self.tasks = []
        genai.configure(api_key=GEMINI_API_KEY)
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
            }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            )
        

        self.chat_session = model.start_chat(
        history=[
        ]
        )
        self.llm = LLM(
            model="gemini/gemini-1.5-pro-latest",
            temperature=0.7
        )
        
    def create_agents(self):
        """Create all SDLC phase agents"""
        # Requirement Analysis Agent
        self.agents['req_analyzer'] = Agent(
            role='Senior Requirements Architect',
            goal='Transform ambiguous inputs into clear specifications',
            backstory="Expert in analyzing requirements with technical precision",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )

        # Design Agent
        self.agents['design_craft'] = Agent(
            role='Chief Systems Architect',
            goal='Create optimal system designs',
            backstory="Experienced architect with modern design pattern expertise",
            llm=self.llm,
            verbose=True
        )

        # Development Agent
        self.agents['code_mate'] = Agent(
            role='Principal Developer',
            goal='Generate production-quality code',
            backstory="Seasoned developer with multi-language expertise",
            llm=self.llm,
            verbose=True
        )

        # Testing Agent
        self.agents['test_genie'] = Agent(
            role='Quality Assurance Lead',
            goal='Ensure comprehensive test coverage',
            backstory="Testing expert with edge-case identification skills",
            llm=self.llm,
            verbose=True
        )

        # Deployment Agent
        self.agents['deploy_wizard'] = Agent(
            role='DevOps Engineer',
            goal='Automate deployment pipelines',
            backstory="CI/CD specialist with cloud deployment experience",
            llm=self.llm,
            verbose=True
        )

        # Maintenance Agent
        self.agents['maintainer_ai'] = Agent(
            role='Systems Maintainer',
            goal='Proactive system monitoring and optimization',
            backstory="Maintenance expert with performance analysis skills",
            llm=self.llm,
            verbose=True
        )

    def create_tasks(self):
        """Create and chain tasks in proper order"""
        self.tasks = []
        
        # Requirement Analysis Task
        req_task = Task(
            description='Analyze requirements for: {user_input}',
            agent=self.agents['req_analyzer'],
            expected_output='Detailed requirements specification document'
        )
        self.tasks.append(req_task)

        # Design Task
        design_task = Task(
            description='Create system design for: {user_input}',
            agent=self.agents['design_craft'],
            context=[req_task],
            expected_output='Technical architecture diagram and design document'
        )
        self.tasks.append(design_task)

        # Development Task
        dev_task = Task(
            description='Develop implementation for: {user_input}',
            agent=self.agents['code_mate'],
            context=[design_task],
            expected_output='Production-ready source code with documentation'
        )
        self.tasks.append(dev_task)

        # Testing Task
        test_task = Task(
            description='Create test plan for: {user_input}',
            agent=self.agents['test_genie'],
            context=[dev_task],
            expected_output='Comprehensive test cases and validation plan'
        )
        self.tasks.append(test_task)

        # Deployment Task
        deploy_task = Task(
            description='Deploy solution for: {user_input}',
            agent=self.agents['deploy_wizard'],
            context=[test_task],
            expected_output='Deployment pipeline configuration'
        )
        self.tasks.append(deploy_task)

        # Maintenance Task
        maint_task = Task(
            description='Create maintenance plan for: {user_input}',
            agent=self.agents['maintainer_ai'],
            context=[deploy_task],
            expected_output='Maintenance schedule and monitoring strategy'
        )
        self.tasks.append(maint_task)

    def assemble_crew(self):
        """Assemble crew with proper configuration"""
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,  # Changed from 2 to True
            manager_llm=self.llm
        )

    def kickoff(self, user_input: str):

        result = self.crew.kickoff(inputs={'user_input': user_input})
        print(f"\nSDLC Execution Result:\n{result}")
        return result

        
if __name__ =="__main__":        
    pass


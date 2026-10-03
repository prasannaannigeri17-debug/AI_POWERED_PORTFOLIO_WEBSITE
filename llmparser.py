import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import resumereader
from typing import List
from pydantic import BaseModel, Field
from inputimeout import inputimeout, TimeoutOccurred
project_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_dir / "api key info" / ".env")
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in the .env file.")
client = Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"
resume_text = resumereader.read(
    str(project_dir / "src" / "llm" / "Prasanna_M_Annigeri_AI_ML_Resume.docx")
)
#1
def askllm(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    ) 
    return response.choices[0].message.content

class ResumeProfile(BaseModel):
    name: str = Field(description="Full legal name of the candidate")
    email: str = Field(description="Email address")
    contact: str = Field(description="Phone or contact number")
    skills: List[str] = Field(default_factory=list, description="Extracted core skills")
    education: List[str] = Field(default_factory=list, description="Degrees and institutions")
    experience: List[str] = Field(default_factory=list, description="Work experience highlights")
    certifications: List[str] = Field(default_factory=list, description="Licenses and certifications")
    projects: List[str] = Field(default_factory=list, description="Notable personal or work projects")


def objectcreation(resume_text):
    # print("WWW")
    System_prompt=f"""You are an experienced hr assistant ,You have to classify the following resume text into a schema you have to stricly follow the texts and do not imagine or create any extra classification . the output format should be {ResumeProfile} schema json object if u are unable to read the pdf return 
    Unable to read docx/pdf please check the format/location of the file"""
    User_prompt=f"""You have to classify this {resume_text} into json using the schema"""
    return askllm(System_prompt,User_prompt)

def processing(resume_text):
    System_prompt=f""" You are an expert ai processing data assistant who understands and processes the json schema . You have to understand all of the content from {resume_text} and only use this content for the solution . No need to imagine the context which is missing from this  content."""
    User_prompt=""" Extract the json information and understand the data for further solution"""
    return askllm(System_prompt,User_prompt)

def InteractiveAssistant(data):
    System_prompt=f""" You are my personal Ai assistant bot you have to answer for all the questions asked by any person taking reference {data} You have to keep it straight and clear and be a friendly ai assistant . Do not invent any skills or answers that isnt related to the data .if u dont know regarding the  concept u can simply add a simple straight answer showing the intrest in learning the  missing skill or anything positive ans which shows the transparency and the  creativity of eagerness of learning the skill despite of not knoeing it . Try to keep the answers not much descriptive and makesure the content is related . For casual hellos and greetings u can reply with the creativity 
    Output format :
    User: input
    Infinity:output"""
    
    try:
        User_prompt = inputimeout(prompt="You : ", timeout=100)
    except TimeoutOccurred:
        print("\nNo response for 100 seconds. Exiting the assistant.")
        return False

    if User_prompt.strip().lower() in ["exit", "quit", "stop"]:
        print("Exiting the assistant.")
        return False

    streaming(System_prompt, User_prompt)
    return True

def streaming(system_prompt,user_prompt):
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,stream=True
        )
    for chunk in stream:
        content=chunk.choices[0].delta.content
        if content:
            print(content,end="",flush=True)
    print()
            
    

def main():
    # Extract the resume once; the separate processing call only added startup delay.
    step2=objectcreation(resume_text)
    print("Hey this infinity prasanna's personal assistant how may i help you : ")

    while InteractiveAssistant(step2):
        pass


if __name__ == "__main__":
    main()
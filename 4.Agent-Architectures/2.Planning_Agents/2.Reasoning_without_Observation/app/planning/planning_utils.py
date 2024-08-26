from langchain_core.prompts import ChatPromptTemplate


def fetch_prompt(task):
    if task =="planner":
        with open("./prompts/planner-prompt.txt", "r") as file:
            prompt = file.read()
    elif task =="solver":
        with open("./prompts/solver-prompt.txt", "r") as file:
            prompt = file.read()            
    return prompt

def create_prompt(task):
    user_prompt=fetch_prompt(task)
    if task=="planner":
        prompt = ChatPromptTemplate.from_messages([("user", user_prompt)])  
    elif task=="solver":
        prompt = prompt       
    return prompt
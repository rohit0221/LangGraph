from langchain_core.prompts import ChatPromptTemplate

def fetch_system_prompt(task):
    if task =="planning":
        with open("./prompts/planning-system-prompt.txt", "r") as file:
            planning_system_prompt = file.read()
    elif task =="replanning":
        with open("./prompts/replanning-system-prompt.txt", "r") as file:
            planning_system_prompt = file.read()            
    return planning_system_prompt

def create_prompt(task):
    system_prompt=fetch_system_prompt(task)

    if task=="planning":
            
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                ("placeholder", "{messages}"),
            ]
        )   
    elif  task=="replanning":
        prompt = ChatPromptTemplate.from_template(
            system_prompt
        )        
    return prompt
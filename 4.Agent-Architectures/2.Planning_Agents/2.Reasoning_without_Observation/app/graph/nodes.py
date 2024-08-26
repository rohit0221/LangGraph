import re

from planning.planning import create_planner
from graph.state import ReWOO

# Regex to match expressions of the form E#... = ...[...]

planner = create_planner()


def get_plan(state: ReWOO):
    task = state["task"]
    result = planner.invoke({"task": task})
    # Find all matches in the sample text
    regex_pattern = r"Plan\:\s*(.*?)\s*(#E\d+)\s*=\s*(\w+)\[(.*?)\]"
    matches = re.findall(regex_pattern, result.content)
    return {"steps": matches, "plan_string": result.content}


def _get_current_task(state: ReWOO):
    if state["results"] is None:
        return 1
    if len(state["results"]) == len(state["steps"]):
        return None
    else:
        return len(state["results"]) + 1


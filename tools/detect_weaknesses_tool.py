from pydantic import BaseModel
from typing import List, Dict, Any
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import json


class Weakness(BaseModel):
    topic: str
    subtopic: str
    accuracy: float
    correct: int
    total: int


class DetectWeaknessesTool(BaseTool):
    name: str = "detect_weaknesses"
    description: str = (
        "Detect topics and subtopics where the user's performance is below a given accuracy threshold."
    )

    def _run(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        threshold = 60
        try:
            analysis = eval(analysis)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input provided to analyze_responses tool.")
        
        weaknesses = []
        for key, perf in analysis.get('topic_performance', {}).items():
            if perf['accuracy'] < threshold:
                topic, subtopic = key.split('/', 1)
                weakness = Weakness(
                    topic=topic,
                    subtopic=subtopic,
                    accuracy=perf['accuracy'],
                    correct=perf['correct'],
                    total=perf['total']
                )
                weaknesses.append(weakness.model_dump())
        return weaknesses





if __name__ == "__main__":
    from langchain_ollama import OllamaLLM

    model = OllamaLLM(
        model="gemma3:12b"
    )

    custom_tools = [
        DetectWeaknessesTool(),
    ]

    agent_with_custom_tools = initialize_agent(
        tools=custom_tools,
        llm=model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    result = agent_with_custom_tools.invoke(
        {
            "input": {
                "score": 50.0,
                "total_questions": 2,
                "correct_count": 1,
                "topic_performance": {
                    "algebra/linear_equations": {
                        "correct": 0.0,
                        "total": 1.0,
                        "accuracy": 0.0
                    },
                    "geometry/triangles": {
                        "correct": 1.0,
                        "total": 1.0,
                        "accuracy": 100.0
                    }
                }
            }
        }
    )
    print(result)
    print(type(result))
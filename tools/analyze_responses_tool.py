from pydantic import BaseModel
from typing import Dict
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import json

class AnalysisResult(BaseModel):
    score: float
    total_questions: int
    correct_count: int
    topic_performance: Dict[str, Dict[str, float]]


class AnalyzeResponsesTool(BaseTool):
    name: str = "analyze_responses"
    description: str = (
        "Analyze a user's quiz responses and compute overall score, total questions, "
        "correct answers count, and accuracy per topic/subtopic."
    )

    def _run(self, data: dict) -> dict:
        try:
            data_dict = eval(data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input provided to analyze_responses tool.")
        
        responses = data_dict.get('responses', [])
        total_questions = len(responses)

        correct_count = sum(
            1 for r in responses if r['selected_option'] == r['correct_option']
        )
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        topic_performance: Dict[str, Dict[str, float]] = {}

        for r in responses:
            key = f"{r['topic']}/{r['subtopic']}"
            if key not in topic_performance:
                topic_performance[key] = {'correct': 0, 'total': 0}

            topic_performance[key]['total'] += 1
            if r['selected_option'] == r['correct_option']:
                topic_performance[key]['correct'] += 1

        for key, stats in topic_performance.items():
            stats['accuracy'] = (stats['correct'] / stats['total']) * 100

        result = AnalysisResult(
            score=score,
            total_questions=total_questions,
            correct_count=correct_count,
            topic_performance=topic_performance
        )
        return result.model_dump()





if __name__ == "__main__":
    from langchain_ollama import OllamaLLM

    model = OllamaLLM(
        model="gemma3:12b"
    )

    custom_tools = [
        AnalyzeResponsesTool(),
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
            "student_id": "12345",
            "quiz_id": "math_001",
            "responses": [
                {
                "question_id": "q1",
                "question": "What is 2 + 2?",
                "selected_option": "B",
                "correct_option": "A",
                "topic": "algebra",
                "subtopic": "linear_equations",
                "difficulty": "medium"
                },
                {
                "question_id": "q2",
                "question": "What is the area of a triangle with base 5 and height 10?",
                "selected_option": "C",
                "correct_option": "C",
                "topic": "geometry",
                "subtopic": "triangles",
                "difficulty": "easy"
                }
            ]
            }
        }
    )
    print(result)
    print(type(result))
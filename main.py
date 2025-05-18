from tools.analyze_responses_tool import AnalyzeResponsesTool
from tools.detect_weaknesses_tool import DetectWeaknessesTool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from utils.read_config_file import read_config_file


OLLAMA_CONFIG_FILE = "./config/ollama_config.yml"
ollama_config = read_config_file(OLLAMA_CONFIG_FILE)

model = OllamaLLM(
    model=ollama_config["model"],
    temperature=ollama_config["temperature"],
)

custom_tools = [
    AnalyzeResponsesTool(),
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













def main():
    print("Hello from mise-a-niveau!")


if __name__ == "__main__":
    main()

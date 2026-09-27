import os
import re

from typing import TypedDict

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from langgraph.graph import StateGraph, END

from budget_tool import check_budget


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


client = genai.Client(
    api_key=api_key
)


# ---------------------------------------------------------
# Gemini Embeddings
# ---------------------------------------------------------

class GeminiEmbeddings(Embeddings):

    def embed_documents(self, texts):

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts
        )

        return [
            embedding.values
            for embedding in result.embeddings
        ]

    def embed_query(self, text):

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return result.embeddings[0].values


# ---------------------------------------------------------
# Load FAISS Vector Store
# ---------------------------------------------------------

embeddings = GeminiEmbeddings()

vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------------------------------------------------------
# Extract Budget Locally
# ---------------------------------------------------------

def extract_budget(question):

    question_lower = question.lower()

    # Match formats like:
    # 80000
    # 80,000
    # 80k
    # 80 K
    # 80 thousand

    match = re.search(
        r"(?:₹|rs\.?|inr)?\s*(\d+(?:,\d{3})*|\d+(?:\.\d+)?)\s*(k|thousand)?",
        question_lower
    )

    if not match:
        return None

    number_text = match.group(1).replace(",", "")
    unit = match.group(2)

    try:
        number = float(number_text)
    except ValueError:
        return None

    if unit in ["k", "thousand"]:
        number *= 1000

    return int(number)


# ---------------------------------------------------------
# Extract Use Case Locally
# ---------------------------------------------------------

def extract_use_case(question):

    question_lower = question.lower()

    keywords = []

    possible_use_cases = [
        "python",
        "programming",
        "coding",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "ai",
        "data science",
        "college",
        "student",
        "gaming",
        "web development",
        "software development",
        "office work",
        "video editing"
    ]

    for use_case in possible_use_cases:

        if use_case in question_lower:

            keywords.append(use_case)

    if keywords:

        return ", ".join(keywords)

    return "general college and programming work"


# ---------------------------------------------------------
# Extract User Requirements
# ---------------------------------------------------------

def extract_information(question):

    budget = extract_budget(question)

    use_case = extract_use_case(question)

    return budget, use_case


# ---------------------------------------------------------
# RAG Search
# ---------------------------------------------------------

def search_laptop_information(
    laptop_names,
    use_case
):

    search_text = (
        "Laptop recommendations for "
        + use_case
        + ". "
        + " ".join(laptop_names)
    )

    results = vector_store.similarity_search(
        search_text,
        k=3
    )

    information = "\n\n".join(
        document.page_content
        for document in results
    )

    return information


# ---------------------------------------------------------
# Generate Final Recommendation
# ---------------------------------------------------------

def generate_recommendation(
    question,
    budget,
    use_case,
    affordable_laptops,
    laptop_information
):

    laptop_text = "\n".join(
        [
            f"{laptop['name']} - ₹{laptop['price']}"
            for laptop in affordable_laptops
        ]
    )

    prompt = f"""
You are a professional laptop recommendation AI agent.

Customer question:
{question}

Maximum budget:
₹{budget}

Main use case:
{use_case}

Laptops within the customer's budget:

{laptop_text}

Retrieved information from the laptop knowledge base:

{laptop_information}

Recommend suitable laptops ONLY from the laptops
listed within the customer's budget.

Consider:

1. Processor performance
2. RAM
3. Storage
4. GPU
5. AI/ML suitability
6. Student and programming needs
7. Customer budget

Do not recommend a laptop above the customer's budget.

Give the answer in this format:

Recommended Laptop:
Price:
Why it fits:
Important hardware:
AI/ML suitability:
Alternative option:

Keep the explanation simple and easy to understand.
"""

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=prompt
        )

        return response.text
    except errors.APIError:
        best_match = affordable_laptops[0]
        alternative = (
            affordable_laptops[1]
            if len(affordable_laptops) > 1
            else best_match
        )

        return (
            "Recommended Laptop:\n"
            f"{best_match['name']}\n\n"
            "Price:\n"
            f"₹{best_match['price']}\n\n"
            "Why it fits:\n"
            f"It is within your ₹{budget} budget and is a practical choice "
            f"for {use_case}.\n\n"
            "Important hardware:\n"
            "Check the processor, RAM, storage, and graphics details in the "
            "retrieved laptop information before purchasing.\n\n"
            "AI/ML suitability:\n"
            "Suitable for learning and lightweight workloads; demanding model "
            "training may require a dedicated GPU.\n\n"
            "Alternative option:\n"
            f"{alternative['name']} - ₹{alternative['price']}"
        )


# ---------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------

class LaptopState(TypedDict, total=False):

    question: str

    budget: int

    use_case: str

    affordable_laptops: list

    laptop_information: str

    recommendation: str


# ---------------------------------------------------------
# Node 1 - Extract User Requirements
# ---------------------------------------------------------

def extract_node(state: LaptopState):

    budget, use_case = extract_information(
        state["question"]
    )

    return {
        "budget": budget,
        "use_case": use_case
    }


# ---------------------------------------------------------
# Node 2 - Budget Tool
# ---------------------------------------------------------

def budget_node(state: LaptopState):

    budget = state.get(
        "budget"
    )

    if budget is None:

        return {
            "affordable_laptops": []
        }

    affordable_laptops = check_budget(
        budget
    )

    return {
        "affordable_laptops":
        affordable_laptops
    }


# ---------------------------------------------------------
# Node 3 - RAG Search
# ---------------------------------------------------------

def rag_node(state: LaptopState):

    laptops = state.get(
        "affordable_laptops",
        []
    )

    if not laptops:

        return {
            "laptop_information":
            "No laptops were found within the specified budget."
        }

    laptop_names = [
        laptop["name"]
        for laptop in laptops
    ]

    information = search_laptop_information(
        laptop_names,
        state["use_case"]
    )

    return {
        "laptop_information":
        information
    }


# ---------------------------------------------------------
# Node 4 - Final Recommendation
# ---------------------------------------------------------

def recommendation_node(state: LaptopState):

    budget = state.get(
        "budget"
    )

    if budget is None:

        return {
            "recommendation":
            "Please provide your maximum laptop budget."
        }

    laptops = state.get(
        "affordable_laptops",
        []
    )

    if not laptops:

        return {
            "recommendation":
            "No laptops are available within your budget."
        }

    recommendation = generate_recommendation(
        state["question"],
        budget,
        state["use_case"],
        laptops,
        state["laptop_information"]
    )

    return {
        "recommendation":
        recommendation
    }


# ---------------------------------------------------------
# Build LangGraph Workflow
# ---------------------------------------------------------

workflow = StateGraph(
    LaptopState
)


workflow.add_node(
    "extract",
    extract_node
)

workflow.add_node(
    "budget_check",
    budget_node
)

workflow.add_node(
    "rag_search",
    rag_node
)

workflow.add_node(
    "recommendation",
    recommendation_node
)


workflow.set_entry_point(
    "extract"
)


workflow.add_edge(
    "extract",
    "budget_check"
)

workflow.add_edge(
    "budget_check",
    "rag_search"
)

workflow.add_edge(
    "rag_search",
    "recommendation"
)

workflow.add_edge(
    "recommendation",
    END
)


laptop_graph = workflow.compile()


# ---------------------------------------------------------
# Main AI Agent
# ---------------------------------------------------------

def laptop_agent(question):

    result = laptop_graph.invoke(
        {
            "question": question
        }
    )

    return result


# ---------------------------------------------------------
# Command Line Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input(
        "\nAsk your laptop recommendation question: "
    )

    result = laptop_agent(
        question
    )

    print("\nBudget:")

    print(
        result.get(
            "budget",
            "Unknown"
        )
    )

    print("\nUse Case:")

    print(
        result.get(
            "use_case",
            "Unknown"
        )
    )

    print("\nAffordable Laptops:")

    laptops = result.get(
        "affordable_laptops",
        []
    )

    for laptop in laptops:

        print(
            laptop["name"],
            "- ₹",
            laptop["price"]
        )

    print("\nFinal Recommendation:")

    print(
        result.get(
            "recommendation",
            "No recommendation"
        )
    )
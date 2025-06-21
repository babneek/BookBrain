import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Set OpenRouter as the base URL
client = openai.OpenAI(
    api_key=openai_api_key,
    base_url="https://openrouter.ai/api/v1/"
)
# Default model for OpenRouter (can be changed to any supported model)
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")

def generate_summary(text: str) -> str:
    prompt = (
        "Please provide a comprehensive, detailed, and multi-paragraph summary of the following text. The summary should cover all key points, main ideas, and important details. Write at least 3 paragraphs.\n\n"
        f"{text}\n\nLong, Detailed Summary:"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] Failed to generate summary: {e}"

def generate_review(text: str) -> str:
    prompt = (
        "Write a thorough, multi-paragraph, critical review of the following content. Discuss its strengths, weaknesses, style, and impact. The review should be long, insightful, and cover all important aspects. Write at least 3 paragraphs.\n\n"
        f"{text}\n\nLong, Detailed Review:"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] Failed to generate review: {e}"

def generate_mcqs(text: str, num_questions: int = 5) -> str:
    prompt = f"""
    You are a helpful assistant designed to create quizzes.
    Based on the text provided, generate exactly {num_questions} multiple-choice questions (MCQs).
    Each question must have a question, 4 options (A, B, C, D), a correct answer, and a brief explanation.

    Here is the required format for each question:
    1. [Question text]?
    A. [Option A]
    B. [Option B]
    C. [Option C]
    D. [Option D]
    Correct answer: [A, B, C, or D]
    Explanation: [Brief explanation of the answer].

    Please strictly follow this format. Do not add any extra text or deviate from the structure.

    Text to use for generating questions:
    ---
    {text}
    ---
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500, # Increased tokens for longer explanations
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] Failed to generate MCQs: {e}" 
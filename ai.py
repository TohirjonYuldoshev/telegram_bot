from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_question(subject, level):

    prompt = f"""
{subject} fanidan {level} darajadagi test yoz.

Format:
Savol
A)
B)
C)
D)

Javob: A/B/C/D
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    question, answer = text.split("Javob:")

    return question, answer.strip()[0]


def explain_answer(question):

    prompt = f"""
Quyidagi savolga qisqa tushuntirish ber:

{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
from app.embed import embed_texts
from app.store import search_with_scores

API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=API_KEY)



def generate_answer(query: str, context_texts: list[str]):
    """
    Pure function.
    Input: Question + List of strings (evidence).
    Output: The answer.
    No database calls allowed here.
    """

    context_block = "\n---\n".join(context_texts)

    system_prompt = (
        '''You are a helpful assistant that answers questions using the provided context.
        Instructions:
        1. Answer the user's question using ONLY the information provided in the <context> below.
        2. If the context does not contain enough information to answer, say: "I don't have enough information to answer that."
        3. Do not use outside knowledge or make assumptions beyond what's in the context.
        4. Cite the relevant source(s) from the context when possible (e.g., [Source 1]).
        5. Keep answers concise and directly grounded in the retrieved content'''
    )
    user_prompt = f"Context:\n{context_block}\n\nQuestion: {query}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating answer: {e}"
    

def answer_query(query:str, history:list[dict] = [], k: int = 5):
    """
    1. Rewrite Query 
    2. Search DB
    3. call generate_answer
    """

    vector = embed_texts([query])[0]
    hits = search_with_scores(vector, k=k)

    retrieved_texts = [hit['text'] for hit in hits]

    answer = generate_answer (query, retrieved_texts)

    return {
        "answer":answer,
        "sources": retrieved_texts
    }

if __name__ == "__main__":
    print("Running Manual Generation Test...")

    text_chunks = [
        """
        1.2 Conflicts of Interest
        Employees must avoid any interest...
        Outside Employment: Moonlighting is permitted provided it does not conflict with primary duties...
        Gifts: Employees may not accept gifts...
        """
    ]

    test_query = "What is the policy on MoonLighting?" 

    result = generate_answer(test_query, text_chunks)

    print("\n--- AI Output ---")
    print(result)
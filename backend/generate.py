import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query, retrieved_chunks):
    """
    Generate a grounded answer using OpenAI GPT.
    - query: user question
    - retrieved_chunks: list of text segments from FAISS
    """
    # Step 1: Construct context string
    context = "\n".join(retrieved_chunks)

    # Step 2: Build prompt
    prompt = f"""
    You are an AI assistant. Use the following context to answer the question.
    Context:
    {context}

    Question: {query}
    Answer:
    """

    # Step 3: Call OpenAI GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight GPT model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )

    # Step 4: Extract answer
    answer = response.choices[0].message.content.strip()
    return answer

if __name__ == "__main__":
    # Example usage
    sample_query = "What is artificial intelligence?"
    sample_chunks = [
        "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines.",
        "These processes include learning, reasoning, and self-correction."
    ]
    answer = generate_answer(sample_query, sample_chunks)
    print("Generated Answer:\n", answer)

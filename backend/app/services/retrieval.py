from openai import OpenAI
client = OpenAI(api_key=Config.OPENAI_API_KEY)
...
    try:
        response = client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        return answer, sources
    except Exception as e:
        print(f"Generation error: {e}")
        return "I'm having trouble generating a response. Please try again later.", []

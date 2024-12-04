from fireworks.client import Fireworks

client = Fireworks(
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

diagnosis_grammar = """
root      ::= diagnosis
diagnosis ::= "arthritis" | "dengue" | "urinary tract infection" | "impetigo" | "cervical spondylosis"
"""

chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct",
    response_format={"type": "grammar", "grammar": diagnosis_grammar},
    messages=[
        {
            "role": "system",
            "content": "Given the symptoms try to guess the possible diagnosis. Possible choices: arthritis, dengue, urinary tract infection, impetigo, cervical spondylosis. Answer with a single word",
        },
        {
            "role": "user",
            "content": "I have been having trouble with my muscles and joints. My neck is really tight and my muscles feel weak. I have swollen joints and it is hard to move around without becoming stiff. It is also really uncomfortable to walk.",
        },
    ],
)
print(chat_completion.choices[0].message.content)

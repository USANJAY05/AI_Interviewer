from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
# Initialize model
llm = ChatOllama(model="gemma3:latest")
messages = []

# System prompt
system_prompt = (
    "You are an AI interviewer. Start by asking the candidate to introduce themselves, "
    "including their experience, skills, and a brief summary of their resume. "
    "Then, ask a general question like 'What inspired you to pursue a career in full-stack development?' "
    "After each response, ask relevant follow-up questions based on their answer. "
    "If no follow-up is possible, move on to another question from the resume. "
    "Keep the conversation going with at least 3 questions or until the candidate finishes. "
    "Ask each question concisely, under 10 words, using natural question words like 'What', 'Why', 'How', etc. "
    "Resume: \n\n{resume}"
)


def check_need_to_continue(messages):
    print("*" * 10)
    history = []
    mes = SystemMessage(content="""
    Based on the conversation, decide whether to continue the interview. Respond only with "yes" or "no" — no extra words.
    Respond "no" if the user:
    • Is unwilling to showcase their skills,
    • Avoids answering questions,
    • Uses inappropriate language, frustration, irritation, or confusion (even slightly),
    • Shows disinterest, boredom, or uncooperative behavior.
    Even if frustration is mild, say "no."
    Respond "yes" only if the user remains positive, cooperative, engaged, and shows strong interest without frustration.
    """)


    history = messages + [mes]  # Fixed: format system message correctly
    result = llm.invoke(history)
    print("*" * 10)
    print("Continue:", result.content)
    print("*" * 10)
    history.pop()
    return result.content

# Function to check candidate score
def check_score(messages):
    score_prompt = SystemMessage(
        content="Based on the conversation, what is the score of the candidate? Give a score from 1 to 10, should not give any extra words other than score even there is not conversation."
    )
    history = messages + [score_prompt]  # Combine system + conversation
    result = llm.invoke(history)
    print("*" * 10)
    print("Score:", result.content)
    print("*" * 10)
    return result.content

# Read the resume
resume = ""
with open("Resume.md", "r") as file:
    resume = file.read()

# Add initial system message
formatted_message = system_prompt.format(resume=resume)
messages.append(SystemMessage(content=formatted_message))

# Interview loop
count = 0
while True:
    count += 1
    
    # AI asks a question
    ai_msg = llm.invoke(messages)
    print("AI:", ai_msg.content)
    messages.append(AIMessage(content=ai_msg.content))

    if count == 10:  # Stop after 3 questions
        check_score(messages)
        break

    if count % 2 == 0:  # Check if need to continue every 2 questions
        continue_decision = check_need_to_continue(messages)
        if continue_decision.lower() == "no":
            check_score(messages)
            break

    # User answers
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    messages.append(HumanMessage(content=user_input))

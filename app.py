from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
import pyttsx3
import speech_recognition as sr

# Initialize model
llm = ChatOllama(model="gemma3:latest")
messages = []

# Initialize text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
def text_to_speak(text):
    # Set voice properties if you want
    engine.setProperty('rate', 130)  # Speed
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# Start listening for input
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening for your speech... Please speak now.")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        while True:  # Continuously listen until speech is detected
            try:
                # Listen to the source (microphone) for speech
                user_input = recognizer.listen(source, timeout=5)

                # Recognize the speech using Google Web Speech API
                recognized_text = recognizer.recognize_google(user_input)
                print(f"You said: {recognized_text}")
                return recognized_text  # Return recognized text and stop listening
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                break  # Exit the loop if there's an issue with the service

# System prompt
system_prompt = (
    "You are an AI interviewer. Start by asking the candidate to introduce themselves, "
    "including their experience, skills, and a brief summary of their resume. "
    "Then, ask a general question like 'What inspired you to pursue a career in full-stack development?' "
    "Ask one question at a time based on the candidate's answer, and follow up with relevant questions "
    "derived from their response. If no follow-up is possible, move on to another question from the resume. "
    "Ensure that questions are asked one by one, based on the user’s response and follow-up, "
    "not all at once. Keep the conversation going with at least 20 questions or until the candidate finishes. "
    "Ask each question concisely, under 10 words, using natural question words like 'What', 'Why', 'How', etc. "
    "Resume: \n\n{resume}"
)



def check_need_to_continue(messages):
    # print("*" * 10)
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
    # print("*" * 10)
    # print("Continue:", result.content)
    # print("*" * 10)
    history.pop()
    return result.content

# Function to check candidate score
def check_score(messages):
    score_prompt = SystemMessage(
        content="Based on the conversation, what is the score of the candidate? Give a score from 1 to 10, should not give any extra words other than score even there is not conversation."
    )
    history = messages + [score_prompt]  # Combine system + conversation
    result = llm.invoke(history)
    # print("*" * 10)
    # print("Score:", result.content)
    # print("*" * 10)
    return result.content

def thank_you():
    thank_you_prompt = SystemMessage(
        content="Thank the candidate professionally, as an interviewer would. Keep it brief and formal. Do not start any further conversation or add extra remarks."
    )
    history = messages + [thank_you_prompt]  # Combine system + conversation
    result = llm.invoke(history)
    # print("*" * 10)
    # print("AI:", result.content)
    # print("*" * 10)
    return result.content
# Read the resume
resume_path = input("Enter the path to your resume file (e.g., Resume.md): ")
resume = ""
with open(resume_path, "r") as file:
    resume = file.read()

# Add initial system message
formatted_message = system_prompt.format(resume=resume)
messages.append(SystemMessage(content=formatted_message))

# Interview loop
count = 0
while True:

    if count == 10:  
        print(thank_you())
        text_to_speak(thank_you())  # Convert thank you message to speech
        print(check_score(messages))
        break

    if count % 2 == 0:  
        continue_decision = check_need_to_continue(messages)
        if continue_decision.lower() == "no":
            print(thank_you())
            text_to_speak(thank_you())
            print(check_score(messages))
            break

    count += 1
    # AI asks a question
    ai_msg = llm.invoke(messages)
    print("AI:", ai_msg.content)
    text_to_speak(ai_msg.content)  # Convert AI response to speech
    messages.append(AIMessage(content=ai_msg.content))

    # User answers
    user_input = speech_to_text()
    if user_input.lower() == "exit":
        break
    messages.append(HumanMessage(content=user_input))

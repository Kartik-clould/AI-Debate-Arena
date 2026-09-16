import os
from groq import Groq
from dotenv import load_dotenv
from ann_model import train_ann, predict_winner

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt): 
    response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

    return response.choices[0].message.content


def pro_agent(topic):
    prompt = f"""
You are the Pro Agent in a debate.

Your job is to argue IN FAVOUR of the topic.

Topic:
{topic}

Give a clear argument with reasoning and examples.
Do not argue against the topic.
"""

    return ask_ai(prompt)


def con_agent(topic):
    prompt = f"""
You are the Con Agent in a debate.

Your job is to argue AGAINST the topic.

Topic:
{topic}

Give a clear argument with reasoning and examples.
Do not argue in favour of the topic.
"""

    return ask_ai(prompt)


def judge_agent(topic, pro_argument, con_argument):
    prompt = f"""
You are the Judge of a debate.

Topic:
{topic}

Pro Agent argument:
{pro_argument}

Con Agent argument:
{con_argument}

Score both sides from 1 to 10 using these categories:

Quality
Relevance
Reasoning

IMPORTANT:
Return ONLY the scores in exactly this format:

Pro Quality: X
Pro Relevance: X
Pro Reasoning: X
Con Quality: X
Con Relevance: X
Con Reasoning: X

Replace X with a number from 1 to 10.
"""

    return ask_ai(prompt)

def pro_rebuttal(topic, con_argument):
    prompt = f"""
You are the Pro Agent in a debate.

Topic:
{topic}

The Con Agent said:
{con_argument}

Respond to the Con Agent's argument.

Defend your position and point out weaknesses
in the Con Agent's argument.
Keep your response clear and logical.
"""

    return ask_ai(prompt)


def con_rebuttal(topic, pro_argument):
    prompt = f"""
You are the Con Agent in a debate.

Topic:
{topic}

The Pro Agent said:
{pro_argument}

Respond to the Pro Agent's argument.

Defend your position and point out weaknesses
in the Pro Agent's argument.
Keep your response clear and logical.
"""

    return ask_ai(prompt)


def run_debate(topic):

    pro_argument = pro_agent(topic)

    con_argument = con_agent(topic)

    pro_reply = pro_rebuttal(topic, con_argument)

    con_reply = con_rebuttal(topic, pro_reply)

    judge_result = judge_agent(
        topic,
        pro_argument,
        con_reply
    )

    # Extract the six scores from Judge
    scores = extract_scores(judge_result)

    # Train ANN
    model = train_ann()

    # Predict winner using Judge scores
    ann_result = predict_winner(model, scores)

    return {
        "topic": topic,
        "pro_argument": pro_argument,
        "con_argument": con_argument,
        "pro_reply": pro_reply,
        "con_reply": con_reply,
        "judge_result": judge_result,
        "judge_scores": scores,
        "winner": ann_result["winner"],
        "pro_probability": ann_result["pro_probability"],
        "con_probability": ann_result["con_probability"]
    }


def extract_scores(judge_result):
    lines = judge_result.split("\n")

    scores = []

    for line in lines:
        if ":" in line:
            score = int(line.split(":")[1].strip())
            scores.append(score)

    return scores
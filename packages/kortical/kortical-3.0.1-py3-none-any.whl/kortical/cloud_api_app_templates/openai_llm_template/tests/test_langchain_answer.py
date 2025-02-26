"""Tests the methods of LangChainOpenAIAnswerer"""
import numpy as np
import openai
import pytest
from kortical.app import get_app_config


app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
openai_api_key = app_config['openai_api_key']
openai.api_key = openai_api_key

# params for running openai
COMPLETION_API_PARAMS = {
    "temperature": 0.0,  # temperature, higher will introduce randomness
    "max_tokens": 2,  # maximum length of the answer, in tokens
    "model": "gpt-3.5-turbo",  # chatgpt model
    "n": 1,  # number of goes at the request
    "stop": ["\n\n\n\n"],  # stop token to use
}

# prompt to compare two answers to the same question.
COMPARE_TWO_ANSWERS_PROMPT = """Here are two answers to a question:
    
Question: {QUESTION}

Answer 1: {ANSWER1}

Answer 2: {ANSWER2}

Yes or No: Could both of the answers above be answers to the question?"""

# test an enquiry about the chatbot, should reply with some info about how it is.
CONVERSATION1 = [
    {"role": "assistant", "content": "Hi, how can I help?"},
    {"role": "user", "content": "How are you?"}
]
ANSWER1 = "I am Paul Graham Bot, a chatbot designed to help users understand and explore Paul Graham's essays. I am functioning correctly and ready to assist you with any questions you may have. Thank you for asking!"

# test an incomplete question, should state that it can't be answered
CONVERSATION2 = [
    {"role": "assistant", "content": "Hi, how can I help?"},
    {"role": "user", "content": "How can I?"}
]
ANSWER2 = 'I\'m sorry, the question "How can I?" is too broad and unclear. Can you please provide more context or specify what you are trying to achieve?'

# test a regular question
CONVERSATION3 = [
    {"role": "assistant", "content": "Hi, how can I help?"},
    {"role": "user", "content": "How can I start a startup?"}
]
ANSWER3 = 'Starting a startup involves three key elements: having good people, making something customers want, and spending as little money as possible. It is important to find something that is missing in your own life and supply that need.\n\nQuote: "You need three things to create a successful startup: to start with good people, to make something customers actually want, and to spend as little money as possible."\n\nRelated Questions:\n- What are the advantages of starting a startup?\n  - How can I find something that is missing in my own life?\n  - What are the key elements of a successful startup?\n\nFor more information, see these links:\n - How to Start a Startup - http://www.paulgraham.com/start.html\n - Why to Not Not Start a Startup - http://www.paulgraham.com/notnot.html\n - How to Make Wealth - http://www.paulgraham.com/wealth.html'

# test a request for more information, should return more info on the above question
CONVERSATION4 = [
    {"role": "assistant", "content": "Hi, how can I help?"},
    {"role": "user", "content": "How can I keep myself sharp as I get older?"},
    {"role": "assistant", "content": 'One way to keep yourself sharp as you get older is to cultivate a habit of impatience about the things you most want to do. Don\'t wait before climbing that mountain or writing that book or visiting your mother. You can also try to slow time somewhat by paying closer attention to the time you have and savoring what you have.'},
    {"role": "user", "content": "can you tell me more?"}
]
ANSWER4 = 'One way to cultivate impatience and pay closer attention to time is to set goals and deadlines for yourself. This will help you stay focused and motivated to complete tasks. Another way is to take time to savor the moments in life, such as spending time with family or friends, or taking a break to appreciate the beauty of nature. Finally, you can challenge yourself to try new things and take risks, as this can help you stay sharp and engaged.\n\nQuote: "It\'s easy to let the days rush by. The "flow" that imaginative people love so much has a darker cousin that prevents you from pausing to savor life amid the daily slurry of errands and alarms."\n\nRelated Questions:\n- What are some ways to set goals and deadlines?\n- How can I savor the moments in life?\n- What are some risks I can take to stay sharp?\n\nFor more information, see these links:\n- Life is Short - http://www.paulgraham.com/vb.html\n- The Bus Ticket Theory of Genius - http://www.paulgraham.com/genius.html\n- The Power of the Marginal - http://www.paulgraham.com/marginal.html'

CONVERSATIONS_WITH_ANSWERS = [
    (CONVERSATION1, ANSWER1),
    (CONVERSATION2, ANSWER2),
    (CONVERSATION3, ANSWER3),
    (CONVERSATION4, ANSWER4),
]


@pytest.mark.unit
def test_init(langchain_question_answerer):
    """Tests that the class initializes successfully."""
    # gets correct api key
    assert langchain_question_answerer.api_key == openai_api_key
    # we have read in the correct data
    assert len(langchain_question_answerer.docsearch.documents) == 3252


@pytest.mark.unit
@pytest.mark.parametrize("conversation,expected_answer", CONVERSATIONS_WITH_ANSWERS)
def test_answer_question(conversation, expected_answer, langchain_question_answerer):
    """Tests that the question answers are expected.

    This is done by asking GPT3 to compare the answers, and decide if they could be answers to the same question.
    We use this approach as there is always some randomness when generating output using LLMs, so answers may
    very slightly.

    Args:
        conversation: List of dictionaries giving the conversation between a user and a chatbot.
        expected_answer: The answer we would expect.
        langchain_question_answerer: The LangChain question answering object to use.
    """
    # test that answer is as expected
    # due to openai outputs being non-deterministic, we ask chatgpt to compare the answers
    retry_count = 0
    while retry_count < 5:
        # server may be busy, try 5 times to answer
        answer = langchain_question_answerer.answer_question(conversation)
        if answer != "I'm sorry, there was a problem. Can you ask me again?":
            break
        retry_count += 1
    msg = COMPARE_TWO_ANSWERS_PROMPT.replace(
        "{ANSWER1}", answer
    ).replace(
        "{ANSWER2}", expected_answer
    ).replace(
        "{QUESTION}", conversation[-1]["content"].strip()
    )
    msgs = [
        {
            "role": "user",
            "content": msg
        }
    ]
    retry_count = 0
    while retry_count < 5:
        # server may be busy, try 5 times to answer
        try:
            comparison_output = openai.ChatCompletion.create(
                messages=msgs, **COMPLETION_API_PARAMS
            )["choices"][0]["message"]["content"].strip().lower()
            break
        except openai.error.RateLimitError as e:
            pass
        retry_count += 1
    assert comparison_output == "yes"

"""Endpoints script for chatbot app, taking a conversation and return the answer."""
from flask import Response, request

from module_placeholder.authentication import safe_api_call
from module_placeholder.question_answering.langchain_answer import LangChainOpenAIAnswerer


# initialize the question answering module
langchain_answerer = LangChainOpenAIAnswerer()


def register_routes(app):

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/chat', methods=['post'])
    @safe_api_call
    def chat():
        conversation = request.json['conversation']
        answer = langchain_answerer.answer_question(conversation)
        return Response(answer)

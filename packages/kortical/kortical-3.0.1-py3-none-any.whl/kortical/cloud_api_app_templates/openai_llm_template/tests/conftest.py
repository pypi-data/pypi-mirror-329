import pytest
from module_placeholder.main import create_app
from module_placeholder.question_answering.langchain_answer import LangChainOpenAIAnswerer


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='session')
def langchain_question_answerer():
    """Creates a langchain question answering object."""
    # this should either initialize the class, or raise an error if openai servers are busy
    # we don't control when the exception will raise, inside the init function we retry 5 times
    langchain_question_answerer = LangChainOpenAIAnswerer(persist_dir=".chroma_db_tmp")
    return langchain_question_answerer

"""Answer questions using langchain"""
import json
import logging
import re
from typing import List, Optional, Tuple

import openai

from kortical.app import get_app_config

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.prompts.prompt import PromptTemplate

from module_placeholder.helpers.root_dir import from_root_dir
from module_placeholder.logging import logging_config
from module_placeholder.question_answering.utils import (
    ChatVectorDbChainUsingChat, PandasCsvLoader, InMemoryVectorStore, get_chat_history
)
from module_placeholder.question_answering.prompts import QA_PROMPT, RELATE_QUESTION_PROMPT


# default params for openai answer generation
TEMPERATURE = 0
MAX_TOKENS = 500

logging_config.init()
logger = logging.getLogger(__name__)

# Kortical app config
app_config = get_app_config(format='yaml')
openai_api_key = app_config['openai_api_key']

openai.api_key = openai_api_key


def validate_openai_key() -> None:
    """Validates a users openai api key.

    Raises:
        openai.error.AuthenticationError: They key was not valid.
    """
    try:
        openai.Model.list()
    except openai.error.AuthenticationError as e:
        # failed due incorrect
        logger.error("OpenAI AuthenticationError:" + e.user_message)
        raise


class LangChainOpenAIAnswerer(object):
    """Class for answering questions using langchain and openai.

    Args:
       config: Config dict. Must contain:
               - data_file_name: filename for documents.
               - openai_api_key: OpenAI API key.

    Attributes:
        api_key: OpenAI api key.
        docsearch: Docsearch object, for semantic search for finding best context docs.
        chain: Langchain chain for answering questions.

    Raises:
        openai.error.AuthenticationError: The user provided an incorrect OpenAI api key.
    """
    def __init__(self, persist_dir: Optional[str] = None):
        """Initialize the object."""
        # set api key
        self.api_key = openai_api_key
        openai.api_key = self.api_key
        # check that the key is valid
        validate_openai_key()
        # setup chain for answering a question
        self._setup_chain()

    def _setup_docsearch(self) -> None:
        """Sets up the langchain docsearch using openai embeddings and input documents."""
        # read in documents
        documents_file_path = from_root_dir(f"data/{app_config['documents_file_name']}")
        csv_loader = PandasCsvLoader(documents_file_path)
        documents = csv_loader.load()
        # load document embeddings
        embeddings_file_path = from_root_dir(f"data/{app_config['embeddings_file_name']}")
        with open(embeddings_file_path, "r") as f:
            document_embeddings = json.load(f)
        # get embedding function
        embedding_function = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.docsearch = InMemoryVectorStore.from_documents(
            documents=documents,
            embedding_function=embedding_function,
            document_embeddings=document_embeddings,
        )

    def _setup_chain(self) -> None:
        """Sets up the langchain chain."""
        qa_prompt = PromptTemplate(
            template=QA_PROMPT.replace(
                "__PlaceHolderBot__", app_config.get("bot_name", "an AI Chatbot")
            ).replace(
                "__PlaceHolderTask__", app_config.get("bot_task", "answer questions")
            ),
            input_variables=["context", "question"]
        )
        relate_question_prompt = PromptTemplate.from_template(RELATE_QUESTION_PROMPT)
        # setup document search
        self._setup_docsearch()
        # setup the chain
        self.chain = ChatVectorDbChainUsingChat.from_llm(
            OpenAIChat(openai_api_key=self.api_key,
                       temperature=app_config.get('output_temperature', TEMPERATURE),
                       max_tokens=app_config.get('output_max_tokens', MAX_TOKENS)),
            self.docsearch,
            return_source_documents=True,
            get_chat_history=get_chat_history,
            qa_prompt=qa_prompt,
            condense_question_prompt=relate_question_prompt
        )

    def answer_question(self, conversation_list: List[dict]) -> str:
        """Answers a question.

        As well as the answer, links to the documents used to answer the question are returned.

        Args:
            conversation_list: The conversation up to this point, as a list of dictionaries.
                               These have the form: {role: user/assistant, content: question/answer}.

        Returns:
            The answer to the question.
        """
        # assume the final entry in the conversation is the most recent question.
        question = conversation_list[-1]["content"].strip()
        if question == "":
            # no question asked
            return "I'm sorry, your question was blank. Can you ask me something else?"
        try:
            # try to answer the question
            # chat history excludes the most recent question, as we send that down as question.
            result = self.chain({"question": question, "chat_history": conversation_list[:-1]})
        except openai.error.RateLimitError as e:
            # there was a problem, probably with openai server
            logger.error(e)
            return "I'm sorry, there was a problem. Can you ask me again?"
        answer = result["answer"].strip()

        answer += "\n\nFind out more:\n" + "\n".join(
            f"{i + 1}. {line}" for i, line in enumerate(
                set(
                    [
                        f"<a href=\"{document.metadata['source']}\" target=\"_blank\">{document.metadata['title']}</a>"
                        for document in result["source_documents"]
                    ]
                )
            )
        )
        return answer.strip().replace("\n", "<br/>")

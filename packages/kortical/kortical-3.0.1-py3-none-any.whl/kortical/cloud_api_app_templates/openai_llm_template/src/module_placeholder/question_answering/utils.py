import re
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from langchain.chains.chat_vector_db.base import ChatVectorDBChain
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore


def get_chat_history(chat_history: List[Dict[str, str]]) -> str:
    """Help function for formatting chat history for langchain.
    
    The chat is outputted as a string of the form:
    User: question1
    Assistant: answer1
    User: question2
    Assistant: answer2 ....
    
    Args:
        chat_history: A list of chat entries. Each entry as the form:
                      {role: {user or assistant}: content: question or answer}.
    
    Returns:
        A string representation of the chat to date.
    """
    buffer = ""
    for chat_line in chat_history:
        if chat_line["role"] == "user":
            buffer += f"\nUser: {chat_line['content']}"
        elif chat_line["role"] == "assistant":
            content = re.split(r'Quote:|Question suggestions:|Find out more:', chat_line['content'])[0].replace('<br/>', '\n').strip()
            buffer += f"\nAssistant: {content}"
    return buffer.strip()


class ChatVectorDbChainUsingChat(ChatVectorDBChain):
    """Update to ChatVectorDBChain using chatGPT functionality."""

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        question = inputs["question"]
        _get_chat_history = self.get_chat_history or get_chat_history
        chat_history_str = _get_chat_history(inputs["chat_history"])
        vectordbkwargs = inputs.get("vectordbkwargs", {})
        if chat_history_str:
            new_question = self.question_generator.run(
                question=question, chat_history=chat_history_str
            )
            if "nothing to do" in new_question.lower():
                new_question = question
        else:
            new_question = question
        docs = self.vectorstore.similarity_search(
            new_question, k=self.top_k_docs_for_context, **vectordbkwargs
        )
        new_inputs = inputs.copy()
        new_inputs["question"] = new_question
        new_inputs["chat_history"] = chat_history_str
        answer, _ = self.combine_docs_chain.combine_docs(docs, **new_inputs)
        if self.return_source_documents:
            return {self.output_key: answer, "source_documents": docs}
        else:
            return {self.output_key: answer}


class PandasCsvLoader(BaseLoader):
    """Loads a CSV file into a list of documents using pandas.
    
    Each row in the csv file is a document or a chunk of a document. It should have
    the following columns:
    - content: Document text.
    In addition, it can have the following optional columns.
    - title: The title of the document or document chunk.
    - source: A path or link to the source material.
    
    Args:
        file_path: Path to the csv file.
        pandas_args: Arguments for reading in the dataframe using pandas.
        
    Attributes:
        file_path: Path to the csv file.
        pandas_args: Arguments for reading in the dataframe using pandas.
    """

    def __init__(self, file_path: str, pandas_args: Optional[Dict] = None):
        """Initialize the class."""
        self.file_path = file_path
        if pandas_args is None:
            self.pandas_args = {
                "delimiter": ",",
                "quotechar": '"',
                "index_col": None
            }
        else:
            self.pandas_args = pandas_args

    def load(self) -> List[Document]:
        """Reads in the csv file and loads it into langchain docs.
        
        Returns:
            A list of document objects for each row in the csv file.
        """
        docs = []
        # read in the csv file
        df = pd.read_csv(self.file_path, **self.pandas_args)
        # metadata for each row
        metadatas = df[["content", "source", "title"]].to_dict('records')
        # determine if there is a source or title
        for (ind, row), metadata in zip(df.iterrows(), metadatas):
            metadata["index"] = str(ind)
            docs.append(
                Document(
                    page_content=row["content"],
                    metadata=metadata,
                )
            )
        return docs


class InMemoryVectorStore(VectorStore):
    """Vectorstore stored in memory.
    
    Args:
        documents: List of document objects to look up context from.
        document_embeddings: Embeddings for the documents.
        embedding_function: Function to use to embed queries.

    Attributes:
        documents: List of document objects to look up context from.
        document_embeddings: Embeddings for the documents.
        embedding_function: Function to use to embed queries.
    """

    def __init__(
        self,
        documents: List[Document],
        document_embeddings: Dict[int, List],
        embedding_function: Optional[Embeddings] = None
    ) -> None:
        """Initialize the class."""
        self.documents = documents
        # convert embeddings to a numpy array to speed up similarity search
        # make sure has the same order as the documents
        self.document_embeddings = np.array(
            [
                np.array(document_embeddings[i]) for i in [document.metadata["index"] for document in documents]
            ]
        )
        self._embedding_function = embedding_function

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Run similarity search with Chroma.
        
        Args:
            query: Query text to search for.
            k: Number of results to return. Defaults to 4.
            filter: Filter by metadata. Defaults to None.

        Returns:
            List of documents most simmilar to the query text.
        """
        query_embedding = np.array(self._embedding_function.embed_query(query))
        similarity_scores = np.dot(self.document_embeddings, query_embedding)
        inds_best_match = np.argpartition(similarity_scores, -k)[-k:][::-1]
        return [self.documents[i] for i in inds_best_match]
    
    def add_texts(
        self,
        texts: List[str],
        document_embeddings: Dict[int, List],
        embedding: Embeddings,
        metadatas: List[dict],
        **kwargs: Any,
    ) -> None:
        """Not implemented."""
        raise NotImplementedError
    
    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        document_embeddings: Dict[int, List],
        embedding: Embeddings,
        metadatas: List[dict],
        **kwargs: Any,
    ) -> None:
        """Not implemented."""
        raise NotImplementedError

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        document_embeddings: Dict[int, List],
        embedding_function: Embeddings,
        **kwargs: Any,
    ) -> VectorStore:
        """Create an in memory vectorstore from a list of documents.

        Args:
            documents: List of document objects to look up context from.
            document_embeddings: Embeddings for the documents.
            embedding_function: Function to use to embed queries.
            
        Returns:
            The in memory vectorstore.
        """
        in_memory_vectorstore = cls(
            documents=documents,
            document_embeddings=document_embeddings,
            embedding_function=embedding_function,
        )
        return in_memory_vectorstore

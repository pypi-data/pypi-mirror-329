import time
import typing
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

StrBool = Annotated[
    bool, PlainSerializer(lambda x: str(x), return_type=str, when_used="unless-none")
]
ModelName = Literal[
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.3-70b-versatile",
    "mistralai/mixtral-8x7b-instruct-v0.1",
    "sonnet-3.5",
    "opus-3",
    "haiku-3",
    "qwen/qwen-2.5-72b-instruct",
]


StrBool = Annotated[
    bool, PlainSerializer(lambda x: str(x), return_type=str, when_used="unless-none")
]


class Snippet(BaseModel):
    """A class representing a text snippet from a document.

    Attributes:
        field (str): The field name from which the snippet was extracted
        text (str): The actual text content of the snippet
        payload (dict | None): Additional metadata associated with the snippet
        score (float): Relevance or ranking score of the snippet
        snippet_id (str | None): Unique identifier for the snippet
    """

    field: str
    text: str
    payload: dict | None = None
    score: float = 0.0
    snippet_id: str | None = None


class SearchDocument(BaseModel):
    """A class representing a search result document containing snippets.

    Attributes:
        source (str): The source identifier of the document
        document (dict): The complete document data
        snippets (list[Snippet]): List of relevant snippets from the document
        score (float): Overall relevance or ranking score of the document
    """

    source: str
    document: dict
    snippets: list[Snippet]
    score: float = 0.0

    def join_snippet_texts(self, separator: str = " <...> ") -> str:
        """Joins the text of multiple snippets with intelligent separators.

        Consecutive snippets (based on chunk_id) are joined with a space,
        while non-consecutive snippets are joined with the specified separator.

        Args:
            separator (str): The separator to use between non-consecutive snippets.
                Defaults to " <...> ".

        Returns:
            str: The concatenated snippet texts with appropriate separators.
        """
        parts = []
        for i, snippet in enumerate(self.snippets):
            if i > 0:
                if (
                    self.snippets[i - 1].payload["chunk_id"] + 1
                    == self.snippets[i].payload["chunk_id"]
                ):
                    parts.append(" ")
                else:
                    parts.append(separator)
            parts.append(snippet.text)
        return "".join(parts)


class SearchRequest(BaseModel):
    """A class representing a search request configuration.

    Attributes:
        query (str | None): The search query string
        source (str): The data source to search in
        query_language (str | None): Language of the query for language-specific processing
        limit (int): Maximum number of results to return (0-16384)
        offset (int): Number of results to skip for pagination (0-16384)
        filters (dict[str, list[Any]]): Dictionary of filters to apply to the search
        load_cache (StrBool): Whether to load results from cache
        store_cache (StrBool): Whether to store results in cache
        snippet_configs (dict[str, int]): Configuration for snippet sizes by field
        fields (list[str] | None): Specific fields to include in the search
        excluded_fields (list[str] | None): Fields to exclude from the search
        scoring (Literal): Scoring method to use ("default", "temporal", "pr", "quantized_pr")
        collector (Literal): Collection method ("top_docs" or "reservoir_sampling")
        term_field_mapping (dict[str, dict[str, list[str]]] | None): Custom mapping of terms to fields
    """

    query: str | None
    source: str
    query_language: str | None = None
    limit: int = Field(default=10, ge=0, le=1024 * 16)
    offset: int = Field(default=0, ge=0, le=1024 * 16)
    filters: dict[str, list[Any]] = Field(default_factory=dict)
    load_cache: StrBool = False
    store_cache: StrBool = False
    snippet_configs: dict[str, int] = Field(
        default_factory=lambda: {
            "title": 1024,
            "abstract": 1024,
            "content": 1024,
        }
    )
    fields: list[str] | None = None
    excluded_fields: list[str] | None = None
    scoring: Literal["default", "temporal", "pr", "quantized_pr"] = "default"
    collector: Literal["top_docs", "reservoir_sampling"] = "top_docs"
    term_field_mapping: dict[str, dict[str, list[str]]] | None = None


class SearchResponse(BaseModel):
    """A class representing the response from a search request.

    Attributes:
        search_documents (list[SearchDocument]): List of retrieved documents with their snippets
        count (int): Total number of results found
        has_next (bool): Whether there are more results available

    Methods:
        empty_response(): Creates and returns an empty search response
    """

    search_documents: list[SearchDocument]
    count: int
    has_next: bool

    @staticmethod
    def empty_response() -> "SearchResponse":
        return SearchResponse(
            search_documents=[],
            count=0,
            has_next=False,
        )


class BaseChunk(BaseModel):
    """A class representing a base chunk of text from a document.

    Attributes:
        document_id (str): Unique identifier for the source document
        field (str): The field name containing the chunk
        chunk_id (int): Sequential identifier for the chunk within the document
        start_index (int): Starting character position of the chunk in the field
        length (int): Length of the chunk in characters
        metadata (dict): Additional metadata associated with the chunk
        updated_at (int): Timestamp of when the chunk was last updated
    """

    document_id: str
    field: str
    chunk_id: int
    start_index: int
    length: int
    metadata: dict
    updated_at: int = Field(default_factory=lambda: int(time.time()))

    def get_unique_id(self) -> str:
        """Generates a unique identifier for the chunk.

        Returns:
            str: A unique string identifier combining document_id, field, and chunk_id
                in the format 'document_id@field@chunk_id'
        """
        return f"{self.document_id}@{self.field}@{self.chunk_id}"


class PreparedChunk(BaseChunk):
    """A prepared chunk that includes the actual text content.

    Attributes:
        text (str): The text content of the chunk
    """

    text: str


class RetrievedChunk(BaseChunk):
    """A retrieved chunk that includes source information and optional text.

    Attributes:
        source (str): The source identifier for the chunk
        text (str | None): The text content of the chunk, if available
        extra_metadata (dict | None): Additional metadata associated with the chunk
    """

    source: str
    text: str | None = None
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class ScoredChunk(BaseModel):
    """A chunk with an associated relevance score and optional vector embedding.

    Attributes:
        chunk (RetrievedChunk): The retrieved chunk
        score (float): Relevance or ranking score
        vector (list[float] | None): Vector embedding of the chunk, if available
    """

    chunk: RetrievedChunk
    score: float = 0.0
    vector: list[float] | None = None


class ScoredGroup(BaseModel):
    """A group of scored chunks from the same document.

    Attributes:
        source (str): The source identifier
        document_id (str): The document identifier
        scored_chunks (list[ScoredChunk]): List of scored chunks from the document
    """

    source: str
    document_id: str
    scored_chunks: list[ScoredChunk]


class LlmConfig(BaseModel):
    """Configuration for the Language Learning Model.

    Attributes:
        model_name (ModelName): Name of the LLM model to use
        api_key (str | None): API key for accessing the model
        max_context_length (int | None): Maximum context length for the model
    """

    model_name: ModelName = "meta-llama/llama-3.3-70b-versatile"
    api_key: str | None = None
    max_context_length: int | None = None

    model_config = ConfigDict(protected_namespaces=tuple())


class RagResponse(BaseModel):
    """Response from a Retrieval-Augmented Generation (RAG) operation.

    Attributes:
        answer (str): The generated response text
        references (list[int]): List of reference indices used in generating the response
        text_related_queries (list[dict[str, str]]): List of related queries with their metadata
    """

    answer: str
    references: list[int]
    text_related_queries: list[dict[str, str]] = Field(default_factory=lambda: [])

    model_config = ConfigDict(protected_namespaces=tuple())


class Range(BaseModel):
    """A class representing a numeric range with left and right bounds.

    Attributes:
        left (int): The lower bound of the range
        right (int): The upper bound of the range
    """

    left: int
    right: int


class RerankConfig(BaseModel):
    """Configuration for result reranking operations.

    Attributes:
        limit (int): Maximum number of results to return after reranking (default: 10)
        reranking_limit (int): Number of top results to consider for reranking (default: 25)
        score_threshold (float | None): Minimum score threshold for results to be included
    """

    limit: int = 10
    reranking_limit: int = 25
    score_threshold: float | None = None


class DiversityConfig(BaseModel):
    """Configuration for result diversity control using clustering.

    Attributes:
        min_cluster_size (int): Minimum number of samples in a cluster (default: 2)
        min_samples (int | None): Minimum samples for core point density calculation
        cluster_selection_epsilon (float): Maximum distance between samples for core point density (default: 0.0)
        alpha (float): Relative density factor for cluster membership (default: 1.0)
        cluster_selection_method (str): Method for selecting clusters (default: "leaf")
    """

    min_cluster_size: int = 2
    min_samples: int | None = None
    cluster_selection_epsilon: float = 0.0
    alpha: float = 1.0
    cluster_selection_method: str = "leaf"


class Query(BaseModel):
    """A class representing a search query with various metadata and processing options.

    Attributes:
        original_query (str | None): The original user query
        reformulated_query (str | None): The processed or reformulated query
        keywords (list[str]): Extracted or relevant keywords
        ids (list[str]): Related document IDs
        is_recent (bool): Flag for recent content queries
        date (tuple[datetime, datetime] | None): Date range for temporal queries
        content_type (str | None): Type of content to search for
        related_queries (list[str]): List of related search queries
        query_language (str | None): Language of the query
        intent (str | None): Intent of the query
    """

    original_query: str | None = None
    reformulated_query: str | None = None
    keywords: list[str] = Field(default_factory=list)
    ids: list[str] = Field(default_factory=list)
    is_recent: bool = False
    date: tuple[datetime, datetime] | None = None
    content_type: str | None = None
    related_queries: list[str] = Field(default_factory=list)
    query_language: str | None = None
    intent: str | None = None

    @staticmethod
    def default_query(query: str | None) -> "Query":
        """Creates a default Query object with minimal configuration.

        Args:
            query (str | None): The query string to use for both original and reformulated fields

        Returns:
            Query: A new Query object with basic configuration
        """
        return Query(
            original_query=query,
            reformulated_query=query,
        )


class QueryClassifierConfig(BaseModel):
    """Configuration for query classification.

    Attributes:
        related_queries (int): Number of related queries to generate (default: 0)
        llm_config (LlmConfig | None): Language model configuration for classification
    """

    related_queries: int = 0
    llm_config: LlmConfig | None = None


class L1Request(BaseModel):
    """First-level search request configuration.

    Attributes:
        source (str): The data source to search in
        limit (int): Maximum number of results to return (0-16384)
        filters (dict[str, list[Any]]): Dictionary of filters to apply to the search
    """

    source: str
    limit: int = Field(default=10, ge=0, le=1024 * 16)
    filters: dict[str, list[Any]] = Field(default_factory=dict)


class RagConfig(BaseModel):
    """Configuration for Retrieval-Augmented Generation (RAG).

    Attributes:
        llm_config (LlmConfig): Language model configuration
        instruction (str | None): Custom instruction for the model
        prompt_template_name (str): Name of the prompt template to use
        target_language (str | None): Target language for translation
        translate_api_key (str | None): API key for translation service
        with_text_related_queries (bool): Whether to include text-related queries
        should_fill_with_abstract (bool): Whether to include document abstracts
        previous_messages (list[dict]): List of previous conversation messages
    """

    llm_config: LlmConfig = Field(default_factory=LlmConfig)
    instruction: str | None = None
    prompt_template_name: str = "default"
    target_language: str | None = None
    translate_api_key: str | None = None
    with_text_related_queries: bool = False
    should_fill_with_abstract: bool = False
    previous_messages: list[dict] = Field(default_factory=lambda: [])


class PipelineRequest(BaseModel):
    """Configuration for the complete search and processing pipeline.

    Attributes:
        query (str | None): Search query string
        sources (list[str]):
        query_classifier (QueryClassifierConfig | None): Query classification configuration
        diversity (DiversityConfig | None): Result diversity configuration
        rag (RagConfig | None): RAG processing configuration
        query_language (str | None): Language of the query
        rerank (RerankConfig | None): Result reranking configuration
    """

    query: str | None = None
    sources: list[str] | None = None
    query_classifier: QueryClassifierConfig | None = None
    diversity: DiversityConfig | None = None
    rag: RagConfig | None = None
    query_language: str | None = None
    rerank: RerankConfig | None = None


class PipelineResponse(BaseModel):
    """Response from the search and processing pipeline.

    Attributes:
        search_documents (list[SearchDocument]): List of retrieved and processed documents
        rag_response (RagResponse | None): Response from RAG processing if enabled
        query (Query | None): Processed query information
    """

    search_documents: list[SearchDocument]
    rag_response: RagResponse | None = None
    query: Query | None = None

    @staticmethod
    def empty_response() -> "PipelineResponse":
        """Creates an empty pipeline response.

        Returns:
            PipelineResponse: An empty response with no search documents
        """
        return PipelineResponse(
            search_documents=[],
        )


class SearchRequestNg(BaseModel):
    query: str
    sources: list[str] | None = None
    filters: dict[str, typing.Any]
    query_language: str | None = None
    snippet_configs: dict[str, int] = Field(
        default_factory=lambda: {
            "title": 1024,
            "abstract": 1024,
            "content": 1024,
        }
    )
    fields: list[str] | None = None
    excluded_fields: list[str] | None = None
    query_classifier: QueryClassifierConfig | None = None
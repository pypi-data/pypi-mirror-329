from datetime import datetime
from typing import Optional, Literal, Dict, List

from pydantic import BaseModel

from pygeai.core.base.models import ChatVariableList, Assistant, WelcomeData


class DocumentMetadata(BaseModel):
    """
    {
      "key": "string",
      "value": "string"
    }
    """
    key: str
    value: str

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value
        }

    def __str__(self):
        metadata = self.to_dict()
        return str(metadata)


class Document(BaseModel):
    id: str
    chunks: str
    name: Optional[str] = None
    extension: str
    index_status: str
    metadata: Optional[List[DocumentMetadata]] = []
    timestamp: Optional[datetime] = None
    url: str

    def to_dict(self):
        document = {
            "id": self.id,
            "chunks": self.chunks,
            "extension": self.extension,
            "indexStatus": self.index_status,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "url": self.url
        }
        return document

    def __str__(self):
        document = self.to_dict()
        return str(document)


class LlmOptions(BaseModel):
    cache: Optional[bool] = False
    frequency_penalty: Optional[float] = None
    max_tokens: Optional[int] = None
    model_name: Optional[str] = None
    n: Optional[int] = None
    presence_penalty: Optional[float] = None
    provider: Optional[str] = None
    stream: Optional[bool] = False
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    type: Optional[str] = ""
    verbose: Optional[bool] = False

    def to_dict(self):
        options = {
            'cache': self.cache,
            'stream': self.stream,
            'verbose': self.verbose
        }
        if self.frequency_penalty is not None:
            options['frequencyPenalty'] = self.frequency_penalty

        if self.max_tokens is not None:
            options['maxTokens'] = self.max_tokens

        if self.model_name is not None:
            options['modelName'] = self.model_name

        if self.n is not None:
            options['n'] = self.n

        if self.presence_penalty is not None:
            options['presencePenalty'] = self.presence_penalty

        if self.provider is not None:
            options['provider'] = self.provider

        if self.temperature is not None:
            options['temperature'] = self.temperature

        if self.top_p is not None:
            options["topP"] = self.top_p

        if self.type is not None:
            options['type'] = self.type

        return options


class Search(BaseModel):
    k: int
    type: Literal["similarity", "mmr"] = "similarity"
    fetch_k: Optional[float] = None  # Valid when using mmr type
    lambda_: Optional[float] = None  # Valid when using mmr type
    prompt: str
    return_source_documents: bool
    score_threshold: float
    template: str

    def to_dict(self):
        search = {
            "k": self.k,
            'type': self.type,
            'prompt': self.prompt,
            'returnSourceDocuments': self.return_source_documents,
            'scoreThreshold': self.score_threshold,
            'template': self.template
        }
        if self.fetch_k is not None:
            search['fetchK'] = self.fetch_k

        if self.lambda_ is not None:
            search['lambda'] = self.lambda_

        return search


class RetrieverOptions(BaseModel):
    type: Literal["vectorStore", "multiQuery", "selfQuery", "hyde", "contextualCompression"]
    search_type: Optional[str] = "similarity"  # Azure AISearch specific, defaults to similarity
    step: Optional[Literal["all", "documents"]] = "all"
    prompt: Optional[str] = None  # Not needed when using vectorStore

    def to_dict(self):
        options = {
            'type': self.type,
            'step': self.step,
        }
        if self.search_type is not None:
            options['searchType'] = self.search_type

        if self.prompt is not None:
            options['prompt'] = self.prompt

        return options


class ChainOptions(BaseModel):
    type: str


class EmbeddingsOptions(BaseModel):
    dimensions: int
    model_name: str
    provider: str
    use_proxy: bool


class IngestionOptions(BaseModel):
    geai_options: Dict
    llama_parse_options: Dict
    provider: str


class SearchOptions(BaseModel):
    history_count: int
    llm: LlmOptions
    search: Search
    retriever: RetrieverOptions
    chain: Optional[ChainOptions] = None
    embeddings: Optional[EmbeddingsOptions] = None
    ingestion: Optional[IngestionOptions] = None
    options: Optional[Dict] = None
    rerank: Optional[Dict] = None
    variables: Optional[ChatVariableList] = None
    vector_store: Optional[Dict] = None

    def to_dict(self):
        options = {
            'historyCount': self.history_count,
            'llm': self.llm.to_dict() if self.llm else None,
            'search': self.search.to_dict() if self.search else None,
            'retriever': self.retriever.to_dict() if self.retriever else None
        }

        if self.chain is not None:
            options['chain'] = self.chain

        if self.embeddings is not None:
            options['embeddings'] = self.embeddings

        if self.ingestion is not None:
            options['ingestion'] = self.ingestion

        if self.options is not None:
            options['options'] = self.options

        if self.rerank is not None:
            options['rerank'] = self.rerank

        if self.variables is not None:
            options['variables'] = self.variables

        if self.vector_store is not None:
            options['vectorStore'] = self.vector_store

        return options


class ChildOptions(BaseModel):
    chunk_size: float
    chunk_overlap: float
    content_processing: Optional[Literal["", "clean"]] = ""

    def to_dict(self):
        options = {
            'chunkSize': self.chunk_size,
            'chunkOverlap': self.chunk_overlap,
        }
        if self.content_processing is not None:
            options['contentProcessing'] = self.content_processing

        return options


class ChildDocumentOptions(BaseModel):
    child_k: float
    child: ChildOptions

    def to_dict(self):
        return {
            'childK': self.child_k,
            'child': self.child.to_dict() if self.child else None
        }


class ChunkOptions(BaseModel):
    chunk_overlap: int
    chunk_size: int

    def to_dict(self):
        return {
            'chunkOverlap': self.chunk_overlap,
            'chunkSize': self.chunk_size
        }


class IndexOptions(BaseModel):
    chunks: ChunkOptions
    use_parent_document: Optional[bool] = False
    child_document: Optional[ChildDocumentOptions] = None  # Valid if use_parent_document is true

    def to_dict(self):
        options = {
            'chunks': self.chunks.to_dict(),
        }
        if self.use_parent_document is not None:
            options['useParentDocument'] = self.use_parent_document

        if self.child_document is not None:
            options['childDocument'] = self.child_document.to_dict()

        return options


class RAGAssistant(Assistant):
    template: Optional[str] = None
    search_options: Optional[SearchOptions] = None
    index_options: Optional[IndexOptions] = None
    welcome_data: Optional[WelcomeData] = None


class UploadDocument(BaseModel):
    path: str
    upload_type: Literal["binary", "multipart"] = "multipart"
    metadata: Optional[dict] = None
    content_type: str


class UploadType:
    BINARY = "binary"
    MULTIPART = "multipart"

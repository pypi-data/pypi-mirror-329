import os, re
import time
import openai
from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceWindowNodeParser, get_leaf_nodes, HierarchicalNodeParser
from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core import load_index_from_storage
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core import PromptTemplate
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.llms.openai import OpenAI

def clean_up_text(content: str) -> str:
    """
    Remove unwanted characters and patterns in text input.

    :param content: Text input.
    
    :return: Cleaned version of original text input.
    """
    # Fix hyphenated words broken by newline
    content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

    # Remove specific unwanted patterns and characters
    unwanted_patterns = [
        "\\n", "  —", "——————————", "—————————", "—————",
        r'\\u[\dA-Fa-f]{4}', r'\uf075', r'\uf0b7'
    ]
    for pattern in unwanted_patterns:
        content = re.sub(pattern, "", content)

    # Fix improperly spaced hyphenated words and normalize whitespace
    content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)
    content = re.sub(r'\s+', ' ', content)

    return content

def build_sentence_window_context(llm, embed_model="local:BAAI/bge-small-en-v1.5"):
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )
    sentence_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=node_parser,
    )
    return sentence_context

def build_sentence_window_index(
    document, llm, embed_model="local:BAAI/bge-small-en-v1.5", save_dir="sentence_index"
):
    # create the sentence window node parser w/ default settings
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )
    sentence_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=node_parser,
    )
    if not os.path.exists(save_dir):
        sentence_index = VectorStoreIndex.from_documents(
            [document], service_context=sentence_context
        )
        sentence_index.storage_context.persist(persist_dir=save_dir)
    else:
        sentence_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=sentence_context,
        )

    return sentence_index


def get_sentence_window_query_engine(
    sentence_index,
    similarity_top_k=6,
    rerank_top_n=2,
):
    # define postprocessors
    postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )

    sentence_window_engine = sentence_index.as_query_engine(
        similarity_top_k=similarity_top_k, node_postprocessors=[postproc, rerank]
    )
    return sentence_window_engine

def build_automerging_context(llm, embed_model="local:BAAI/bge-small-en-v1.5"):
    merging_context = ServiceContext.from_defaults(llm=llm,embed_model=embed_model,)
    return merging_context

def build_automerging_index(
    documents,
    llm,
    embed_model="local:BAAI/bge-small-en-v1.5",
    save_dir="merging_index",
    chunk_sizes=None,
):
    chunk_sizes = chunk_sizes or [2048, 512, 128]
    node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)
    nodes = node_parser.get_nodes_from_documents(documents)
    leaf_nodes = get_leaf_nodes(nodes)
    merging_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)
    
    automerging_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context, service_context=merging_context)

    return automerging_index


def get_automerging_query_engine(
    automerging_index,
    similarity_top_k=12,
    rerank_top_n=2,
):
    base_retriever = automerging_index.as_retriever(similarity_top_k=similarity_top_k)
    retriever = AutoMergingRetriever(
        base_retriever, automerging_index.storage_context, verbose=True
    )
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )
    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )
    return auto_merging_engine

class RAGStringQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""
    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate = PromptTemplate(
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_chat: PromptTemplate = PromptTemplate(
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Chat history is below.\n"
        "---------------------\n"
        "{chat_history}\n"
        "---------------------\n"
        "Given the context information and chat history, and not prior knowledge, "
        "answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )

    def custom_query(self, query_str: str, chat_history=None, max_chat_interactions=5):
        '''
        chat_history: list of dicts. Each dict has keys question and answer.
        '''
        nodes = self.retriever.retrieve(query_str)

        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        if chat_history is not None and len(chat_history) > 0:
            chat_history_str = "\n".join([f"User: {item['question']}\nAssistant: {item['answer']}" for item in chat_history[:max_chat_interactions]])
        else:
            chat_history_str = None
        if chat_history_str:
            response = self.llm.complete(
                self.qa_prompt_chat.format(context_str=context_str, chat_history=chat_history_str, query_str=query_str)
            )
        else:
            response = self.llm.complete(
                self.qa_prompt.format(context_str=context_str, query_str=query_str)
            )
        return str(response), nodes

def translate_chunk(chunk, source_lang=None, target_lang="es", engine="text-davinci-003"):            
    if source_lang is None:
        trans_prompt = f"Translate the following text into {target_lang} while preserving its meaning and tone. Detect the original language automatically"
    else:
        trans_prompt = f"Translate the following text from {source_lang} to {target_lang} while preserving its meaning and tone."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": trans_prompt},
            {"role": "user", "content": chunk}
        ]
    )
    trans_text = response.choices[0].message.content.strip()
    return trans_text

def translate_document(chunks, source_lang="en", target_lang="es"):
    translated_text = ""
    
    for i, chunk in enumerate(chunks):
        print(f"Translating chunk {i + 1}/{len(chunks)}")
        try:
            translation = translate_chunk(chunk, source_lang, target_lang)
            translated_text += translation + "\n\n"
            time.sleep(1)  # Respectful delay to avoid rate limits
        except Exception as e:
            print(f"Error translating chunk {i + 1}: {e}")
            time.sleep(5)  # Wait before retrying if there's an error

    return translated_text

from langchain.vectorstores.chroma import Chroma
from langchain.docstore.document import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from memory import Memory

embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

database = Chroma(embedding_function = embedding_func, persist_directory= 'database/testdb' , 
                                relevance_score_fn='similarity_search_with_score')
memory = Memory(k=5, vector_db=database)

experience1 = "Kshitiz is god and he will be god."
metadata1 = {
    'tool_name': "kshitiz"
}
experience2 = "Jatin is god and he will be god."
metadata2 = {
    'tool_name': "jatin"
}
doc1 = Document(page_content=experience1 , metadata=metadata1)
doc2 = Document(page_content=experience2 , metadata=metadata2)

memory.stage(docs=doc1)
memory.stage(docs=doc2)
memory.push()

filter = {
    'tool_name': 'kshitiz'
}
res = memory.pull(query="is there a god?",filter=filter)
print(res)


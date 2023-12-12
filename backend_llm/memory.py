from queue import Queue
from langchain.docstore.document import Document

class Memory():
    def __init__(self,vector_db, k=5) -> None:
        self.queue = Queue(maxsize=10) # current List to be added to Long Term Memory
        self.k = k
        self.vector_db = vector_db
    
    def stage(self, docs:Document):
        self.queue.put(docs)
        print("\033[91m {}\033[00m" .format('Document Staged in Memory...'))
        
    def push(self):
        print(f"Pushing {self.queue.qsize()} Documents...")
        while not self.queue.empty():
            self.vector_db.add_documents([self.queue.get()])
        
    def pull(self, query:str,filter = None):
        if filter == None:
            results  = self.vector_db.similarity_search(query, k=self.k , search_type='similarity')
        else:
            results  = self.vector_db.similarity_search(query, k=self.k , search_type='similarity',filter = filter)

        return results
    
    def clear(self):
        '''
        Clears all items from the queue.
        '''

        self.queue = Queue(maxsize=10)
import os
from random import randint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PlagiarismChecker:
    def __init__(self, path: str):
        self.path = path
        self.similarity = None
        self.vectors = None
        self.files = None

    def read_files(self):
        self.files = [doc for doc in os.listdir(self.path) if doc.endswith(".txt")]
        return [open(os.path.join(self.path, file)).read() for file in self.files]

    def delete_read_files(self):
        self.files = [doc for doc in os.listdir(self.path) if doc.endswith(".txt")]
        for file in self.files:
            os.remove(os.path.join(self.path, file))
        os.rmdir(self.path)

    def data_transformer(self, data: list):
        if not len(data) == 0:
            vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
            self.similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
            vectors = vectorize(data)
            self.vectors = list(zip(self.files, vectors))

    def check_plagiarism(self):
        result = set()
        for a, text_vector_a in self.vectors:
            new_vectors = self.vectors.copy()
            current_index = new_vectors.index((a, text_vector_a))
            del new_vectors[current_index]
            for b, text_vector_b in new_vectors:
                sim_score = self.similarity(text_vector_a, text_vector_b)[0][1]
                pair = sorted((a, b))
                score = (pair[0], pair[1], sim_score)
                result.add(score)

        return result

    def get_results(self):

        data = self.read_files()
        self.delete_read_files()
        self.data_transformer(data)
        return self.check_plagiarism()
    
    

if __name__ == "__main__":

    path = os.path.join(os.getcwd(), "files", str(randint(1000000, 9999999)))
    pc = PlagiarismChecker(path)
    result = pc.get_results()
    for item in result:
        print(item[0], item[1], round(item[2] * 100, 2))

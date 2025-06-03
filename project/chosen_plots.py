from sentence_transformers import SentenceTransformer, util
import json
import torch


class RecMa():
    def __init__(self, query, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.query = query

        data_corpus = torch.load("corpus_embeddings(1).pt", map_location="cpu")
        self.corpus = data_corpus["corpus"]
        self.model = SentenceTransformer(model_name)
        self.query_embeddings = self.model.encode(self.query, convert_to_tensor=True)
        self.corpus_embeddings = data_corpus["embeddings"]

    def sim_rate(self):
        scores = util.cos_sim(self.query_embeddings, self.corpus_embeddings)[0]
        return [(score.item(), plot) for score, plot in zip(scores, self.corpus)]

    def satisfied_plot(self, threshold=0.4):
        output = [sim[1] for sim in self.sim_rate() if sim[0] > threshold]

        return output


class GenreMatch():
    def __init__(self, query, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.query = query
        with open("data/genre_emotion_map", "r") as file:
            genre_emotion_map = json.load(file)

        self.corpus = list(genre_emotion_map.keys())
        self.model = SentenceTransformer(model_name)
        self.query_embeddings = self.model.encode(self.query, convert_to_tensor=True)
        self.corpus_embeddings = self.model.encode(list(genre_emotion_map.values()), convert_to_tensor=True)

    def sim_rate(self):
        scores = util.cos_sim(self.query_embeddings, self.corpus_embeddings)[0]
        result = [(score.item(), genre) for score, genre in zip(scores, self.corpus)]
        return max(result, key=lambda x: x[0])[1]


from math import log


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self.lowercase = lowercase
        self.ngram_size = ngram_size
        self._vocabulary = {}
        self._ready = False

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, words):
        self._vocabulary = words.copy()
        self._ready = bool(words)

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}
        self._ready = False

    def add_word(self, word):
        if word not in self.vocabulary:
            self.vocabulary[word] = len(self.vocabulary)
        return self.vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        tokens = []
        for i in range(len(words) - self.ngram_size + 1):
            tokens.append(" ".join(words[i:i + self.ngram_size]))
        return tokens

    def fit(self, corpus):
        tokens = []
        for text in corpus:
            tokens.extend(self.tokenize(text))

        if not tokens:
            raise ValueError("В корпусе нет токенов")

        self._vocabulary = {}
        for word in tokens:
            self.add_word(word)
        self._ready = True
        return self

    def transform(self, corpus):
        if not self._ready:
            raise RuntimeError("Сначала обучите модель или задайте словарь")

        matrix = []
        for text in corpus:
            row = [0] * len(self.vocabulary)
            for word in self.tokenize(text):
                if word in self.vocabulary:
                    row[self.vocabulary[word]] += 1
            matrix.append(row)
        return matrix

    def get_feature_names(self):
        return sorted(self.vocabulary, key=self.vocabulary.get)

    def fit_transform(self, corpus):
        corpus = list(corpus)
        return self.fit(corpus).transform(corpus)

    def to_dict(self):
        return {
            "lowercase": self.lowercase,
            "ngram_size": self.ngram_size,
            "vocabulary": self.vocabulary.copy(),
        }

    @classmethod
    def from_dict(cls, state):
        model = cls(
            lowercase=state["lowercase"], ngram_size=state["ngram_size"]
        )
        model.vocabulary = state["vocabulary"]
        return model


class BinaryVectorizer(CountVectorizer):
    def transform(self, corpus):
        matrix = super().transform(corpus)
        for row in matrix:
            for index, count in enumerate(row):
                row[index] = int(count > 0)
        return matrix

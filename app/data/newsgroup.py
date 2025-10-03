import numpy as np

from sklearn.datasets import fetch_20newsgroups


class Dataset:
    def __init__(self):
        self.ds = fetch_20newsgroups(
            subset="train", remove=("headers", "footers", "quotes")
        )

    def get_n_random_docs(self, n):
        assert 0 <= n <= len(self.ds.data), "Number of documents is invalid."

        ids = np.arange(len(self.ds.data))
        np.random.shuffle(ids)

        docs = [self[idx] for idx in ids[:n]]

        return docs

    def __getitem__(self, idx):
        return (self.ds.target_names[self.ds.target[idx]], self.ds.data[idx])

    def __len__(self):
        return len(self.ds.data)


if __name__ == "__main__":
    ds = Dataset()
    n_docs = ds.get_n_random_docs(10)
    print(n_docs)

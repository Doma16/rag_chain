from data.newsgroup import Dataset
import requests
import argparse

URL = "http://127.0.0.1:8000/"
NUMBER_OF_DOCS = 30


def login(username, password):
    res = requests.post(
        url=URL + "login", json={"username": username, "password": password}
    )
    return res.cookies


def get_docs():
    ds = Dataset()
    docs = ds.get_n_random_docs(100)
    return docs


def _upload_doc(doc, cookie):
    res = requests.post(
        url=URL + "documents/upload",
        cookies=cookie,
        json={"filename": doc[0], "content": doc[1]},
    )
    return res.status_code


def upload_docs(docs, cookie):
    for doc in docs:
        code = _upload_doc(doc, cookie)
        if code != 200:
            break


def main(args):
    cookie = login(args.username, args.password)
    docs = get_docs()
    upload_docs(docs, cookie)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    return parser.parse_args()


if __name__ == "__main__":
    main(_parse_args())

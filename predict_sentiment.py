from polyglot.text import Text

from polyglot.downloader import downloader

downloader.download("embeddings2.en", quiet=True)
downloader.download("embeddings2.ru", quiet=True)
downloader.download("embeddings2.uk", quiet=True)
downloader.download("sentiment2.en", quiet=True)
downloader.download("sentiment2.ru", quiet=True)


def get_polarity_coefficient(text):
    return Text(text, hint_language_code='ru').polarity
import ssl
import download_nltk_data

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

download_nltk_data.download('punkt')
download_nltk_data.download('wordnet')
download_nltk_data.download('brown')
download_nltk_data.download('averaged_perceptron_tagger')
download_nltk_data.download('conll2000')
download_nltk_data.download('movie_reviews')

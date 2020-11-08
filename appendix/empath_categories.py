from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from empath import Empath
lexicon = Empath()

lexicon.create_category("multi_flatland", ["colors", "shapes", "geometry", "dimension", "line"], model="fiction", size=400,
                        write=False)

# lexicon.create_category("multi_ulysses", ["general", "military", "history","army", "soldier"], model="fiction", size=400,
#                         write=False)
#
# lexicon.create_category("multi_panama", ["history", "geography", "south america", "canal", "jungle"], model="fiction", size=400,
#                         write=False)
#
# booklist = ["flatland.txt","ulysses.txt","panama.txt"]
booklist = ["flatland.txt"]

for bookname in booklist:
    open_file = open(bookname, 'r', encoding='utf-8')
    book = open_file.read()
    tokens = word_tokenize(book)
    lowercase_tokens = [t.lower() for t in tokens]
    alphabets = [t for t in lowercase_tokens if t.isalpha()]
    words = stopwords.words("english")
    stopwords_removed = [t for t in alphabets if t not in words]
    lemmatizer = WordNetLemmatizer()
    lem_tokens = [lemmatizer.lemmatize(t) for t in stopwords_removed]
    print(lexicon.analyze(book,categories=["multi_flatland"],normalize=True))
    print(lexicon.analyze(book,categories=["multi_flatland"],normalize=False))
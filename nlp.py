from nltk.stem import WordNetLemmatizer
import spacy
import en_core_web_sm
import string 
from string import punctuation
from collections import Counter

nlp = en_core_web_sm.load()

# print("rocks :", lemmatizer.lemmatize("rocks"))
# #TODO option if noun to not stem

# Load the spaCy English model
# TODO change to lg? python3 -m spacy download en_core_web_lg
nlp = spacy.load('en_core_web_sm')

def text_cleanup(text):
  text = text.lower()
  text = text.replace("\n","")
  # Process the text using spaCy
  doc = nlp(text)
  
  # Extract lemmatized tokens
  lemmatized_tokens = [token.lemma_ for token in doc]
  
  # Join the lemmatized tokens into a sentence
  lemmatized_text = ' '.join(lemmatized_tokens)
  cut_punctuation = punctuation.replace('.','')

  # TODO keep periods eventually for splitting on
  translation_table = dict.fromkeys(map(ord, cut_punctuation), None)

  removed_text = lemmatized_text.translate(translation_table)
  removed_text = removed_text.replace("  ", " ")
  return removed_text
  # split text on periods and newlines, removing whitespace?

def get_hotwords(text, query):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    query_words = query.split()
    # check if word in list or if there is a close enough similarity score
    # combined relevance between words?
    # checks to see if each word in the text is from the query (for now)
    query_cut_words = ' '.join([word for word in text.split() if word in query_words])
    # result = ' '.join(resultwords)
    doc = nlp(query_cut_words) 
    for token in doc:
        # not stop words to continue
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # type of word is valid
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result

def selection(text, hotwords, orig_text):
  orig_sentences = orig_text.split(".")
  sentences = text.split(".")
  res_sentences = []
  for i, sentence in enumerate(sentences):
    best_hotwords = [0]*len(hotwords)
    for word in sentence.split(" "):
       for j, hotword in enumerate(hotwords):
          if word == hotword[0]:
             # hotword found in sentence
             best_hotwords[j] = 1
    # getting the average between all of hotwords, determining relevance of sentence
    avg_score = sum(best_hotwords) / len(best_hotwords)
    # arbitrary cutoff for adding the sentence
    if avg_score > .85:
      res_sentences.append(orig_sentences[i])
  return res_sentences

# Define a sample text
text = """
When it comes to evaluating the performance of keyword extractors, you can use some of the standard metrics in machine learning: accuracy, precision, recall, and F1 score. However, these metrics don’t reflect partial matches. they only consider the perfect match between an extracted segment and the correct prediction for that tag.
Fortunately, there are some other metrics capable of capturing partial matches. An example of this is ROUGE.
"""
print("Original Text:", text)
new_text = text_cleanup(text)
print("Removed text: ", new_text)

query = """
what performance is the keyword sasdawr
"""

output = set(get_hotwords(new_text, query))
# TODO get least common instead of most?
most_common_list = Counter(output).most_common(10)
for item in most_common_list:
  print(item[0])
print(selection(new_text, most_common_list, text))

# TODO add word2vec

# potentially unnecessary stuff
# max_summary_len = 15
# #prepare a tokenizer for reviews on training data
# y_tokenizer = Tokenizer(num_words=tot_cnt-cnt) 
# y_tokenizer.fit_on_texts(list(y_tr))
# y_val = list(map(lambda x: str(x), y_val))

# #convert text sequences into integer sequences (i.e one hot encode the text in Y)
# y_tr_seq    =   y_tokenizer.texts_to_sequences(y_tr) 
# y_val_seq   =   y_tokenizer.texts_to_sequences(y_val) 

# #padding zero upto maximum length
# y_tr    =   pad_sequences(y_tr_seq, maxlen=max_summary_len, padding='post')
# y_val   =   pad_sequences(y_val_seq, maxlen=max_summary_len, padding='post')

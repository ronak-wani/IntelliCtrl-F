from nltk.stem import WordNetLemmatizer
import spacy
import en_core_web_sm
import string 
from string import punctuation
from collections import Counter
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
from keybert import KeyBERT
import nltk

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

def get_hot_words_keybert(text, query):
   kw_model = KeyBERT()
   # get all hot word data
   hot_words = kw_model.extract_keywords(text, stop_words='english', top_n=-1)
   hot_words = list(filter(lambda hot_word: hot_word[0] in query.split(' '), hot_words))
   # no keywords found in query
   if len(hot_words) == 0:
      return hot_words
   # treat the top hop word as '1', and compare every other hot word to that
   hot_words = list(map(lambda hot_word: (hot_word[0], 1 - (hot_words[0][1] - hot_word[1])), hot_words))
   # TODO cutoff for hot_words, minimum lowness?
   # using hot words, pick the best variables from the query
   # use each word from query, with relevance % being determined from keybert
   # find best instance of each key word in each sentence
   # add/sum the results, getting a score that determines if we return the sentence

   return hot_words

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

def selection_word2vec(text, hot_words, model, orig_text):
  # TODO split on new line too?
  orig_sentences = orig_text.split(".")
  sentences = text.split(".")
  res_sentences = []
  pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
  for i, sentence in enumerate(sentences):
    best_hotwords = [0]*len(hot_words)
    enum_sentence = sentence.split(" ")
    words = nlp(sentence) 
    for word_info in words:
      word = word_info.text
      pos = word_info.pos_
      if pos in pos_tag:
        for j, hot_word in enumerate(hot_words):
            try:
              cur_sim = model.wv.similarity(word, hot_word[0]) 
              adj_sim = cur_sim ** 4
              # print(word, hot_word[0], cur_sim, adj_sim)
              adj_sim = adj_sim * hot_word[1] # multiplying by relevance
              adj_sim += 1 - hot_word[1] # make less relevant words matter less
              if adj_sim > best_hotwords[j]:
                # print(word, hot_word[0], cur_sim)
                best_hotwords[j] = adj_sim
              if cur_sim == 1: # best possible word found
                break
            except Exception as error: # if key not present in sim
              break
    # getting the average between all of hotwords, determining relevance of sentence
    avg_score = sum(best_hotwords) / len(best_hotwords)
    print(best_hotwords, avg_score)
    # arbitrary cutoff for adding the sentence
    if avg_score > .85:
      res_sentences.append(orig_sentences[i])
  # return res_sentences

def tokenizer(text):
  res_tokens = []
  # iterate through each sentence in the file
  for i in sent_tokenize(text):
      temp = []
      # tokenize the sentence into words
      for j in word_tokenize(i):
          temp.append(j.lower())
      res_tokens.append(temp)
  return res_tokens
# Define a sample text
text = """
When it comes to evaluating the performance of keyword extractors, you can use some of the standard metrics in machine learning: accuracy, precision, recall, and F1 score. However, these metrics don’t reflect partial matches. they only consider the perfect match between an extracted segment and the correct prediction for that tag.
Fortunately, there are some other metrics capable of capturing partial matches. An example of this is ROUGE.
"""
sample = open("./alice.txt")
text = sample.read()
text = text.replace("\n", " ")
# print("Original Text:", text)
new_text = text_cleanup(text)

# print("Removed text: ", new_text)

query = """
i want a story about how alice performed best under pressure.
"""
query = text_cleanup(query)
# output = set(get_hotwords(new_text, query))
# # TODO get least common instead of most?
# most_common_list = Counter(output).most_common(10)
# for item in most_common_list:
#   print(item[0])
# print(selection(new_text, most_common_list, text))


# Create CBOW model
model1 = gensim.models.Word2Vec(tokenizer(new_text), min_count=1,
                                vector_size=100, window=5)
# Print results
print("Cosine similarity between 'alice' " +
      "and 'wonderland' - CBOW : ",
      model1.wv.similarity('alice', 'wonderland'))
# print("Cosine similarity between 'perfect' " +
#       "and 'match' - CBOW : ",
#       model1.wv.similarity('perfect', 'match'))
# print("Cosine similarity between 'alice' " +
#       "and 'machines' - CBOW : ",
#       model1.wv.similarity('keyword', 'match'))
 
# Create Skip Gram model
model2 = gensim.models.Word2Vec(tokenizer(new_text), min_count=1, vector_size=100,
                                window=5, sg=1)
 
# Print results
print("Cosine similarity between 'alice' " +
      "and 'wonderland' - Skip Gram : ",
      model2.wv.similarity('alice', 'wonderland'))
# print("Cosine similarity between 'perfect' " +
#       "and 'match' - CBOW : ",
#       model2.wv.similarity('perfect', 'match'))
# print("Cosine similarity between 'alice' " +
#       "and 'machines' - Skip Gram : ",
#       model2.wv.similarity('keyword', 'match'))

new_hotwords = get_hot_words_keybert(new_text, query)
print(new_hotwords)
print(selection_word2vec(new_text, new_hotwords, model2, text))
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

# Twitter-roBERTa-base

This is a RoBERTa-base model trained on ~58M tweets on top of the original RoBERTa-base checkpoint, as described and evaluated in the [_TweetEval_ benchmark (Findings of EMNLP 2020)](https://arxiv.org/pdf/2010.12421.pdf). 
To evaluate this and other LMs on Twitter-specific data, please refer to the [Tweeteval official repository](https://github.com/cardiffnlp/tweeteval).

## Preprocess Text 
Replace usernames and links for placeholders: "@user" and "http".
```python
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
```

## Example Masked Language Model 

```python
from transformers import pipeline, AutoTokenizer
import numpy as np

MODEL = "cardiffnlp/twitter-roberta-base"
fill_mask = pipeline("fill-mask", model=MODEL, tokenizer=MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)

def print_candidates():
    for i in range(5):
        token = tokenizer.decode(candidates[i]['token'])
        score = np.round(candidates[i]['score'], 4)
        print(f"{i+1}) {token} {score}")

texts = [
 "I am so <mask> 😊",
 "I am so <mask> 😢" 
]
for text in texts:
    t = preprocess(text)
    print(f"{'-'*30}\n{t}")
    candidates = fill_mask(t)
    print_candidates()
```

Output: 

```
------------------------------
I am so <mask> 😊
1)  happy 0.402
2)  excited 0.1441
3)  proud 0.143
4)  grateful 0.0669
5)  blessed 0.0334
------------------------------
I am so <mask> 😢
1)  sad 0.2641
2)  sorry 0.1605
3)  tired 0.138
4)  sick 0.0278
5)  hungry 0.0232
```

## Example Tweet Embeddings
```python
from transformers import AutoTokenizer, AutoModel, TFAutoModel
import numpy as np
from scipy.spatial.distance import cosine
from collections import defaultdict

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModel.from_pretrained(MODEL)

def get_embedding(text):
  text = preprocess(text)
  encoded_input = tokenizer(text, return_tensors='pt')
  features = model(**encoded_input)
  features = features[0].detach().cpu().numpy() 
  features_mean = np.mean(features[0], axis=0) 
  return features_mean

MODEL = "cardiffnlp/twitter-roberta-base"

query = "The book was awesome"

tweets = ["I just ordered fried chicken 🐣", 
          "The movie was great", 
          "What time is the next game?", 
          "Just finished reading 'Embeddings in NLP'"]

d = defaultdict(int)
for tweet in tweets:
  sim = 1-cosine(get_embedding(query),get_embedding(tweet))
  d[tweet] = sim

print('Most similar to: ',query)
print('----------------------------------------')
for idx,x in enumerate(sorted(d.items(), key=lambda x:x[1], reverse=True)):
  print(idx+1,x[0])
```
Output: 

```
Most similar to:  The book was awesome
----------------------------------------
1 The movie was great
2 Just finished reading 'Embeddings in NLP'
3 I just ordered fried chicken 🐣
4 What time is the next game?
```

## Example Feature Extraction 

```python
from transformers import AutoTokenizer, AutoModel, TFAutoModel
import numpy as np

MODEL = "cardiffnlp/twitter-roberta-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

text = "Good night 😊"
text = preprocess(text)

# Pytorch
model = AutoModel.from_pretrained(MODEL)
encoded_input = tokenizer(text, return_tensors='pt')
features = model(**encoded_input)
features = features[0].detach().cpu().numpy() 
features_mean = np.mean(features[0], axis=0) 
#features_max = np.max(features[0], axis=0)

# # Tensorflow
# model = TFAutoModel.from_pretrained(MODEL)
# encoded_input = tokenizer(text, return_tensors='tf')
# features = model(encoded_input)
# features = features[0].numpy()
# features_mean = np.mean(features[0], axis=0) 
# #features_max = np.max(features[0], axis=0)

```

### BibTeX entry and citation info

Please cite the [reference paper](https://aclanthology.org/2020.findings-emnlp.148/) if you use this model.

```bibtex
@inproceedings{barbieri-etal-2020-tweeteval,
    title = "{T}weet{E}val: Unified Benchmark and Comparative Evaluation for Tweet Classification",
    author = "Barbieri, Francesco  and
      Camacho-Collados, Jose  and
      Espinosa Anke, Luis  and
      Neves, Leonardo",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.findings-emnlp.148",
    doi = "10.18653/v1/2020.findings-emnlp.148",
    pages = "1644--1650"
}
```
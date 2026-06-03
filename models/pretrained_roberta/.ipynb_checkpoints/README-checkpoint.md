# Twitter-roBERTa-base

This is a roBERTa-base model trained on ~58M tweets, described and evaluated in the [_TweetEval_ benchmark (Findings of EMNLP 2020)](https://arxiv.org/pdf/2010.12421.pdf). To evaluate this and other LMs on Twitter-specific data, please refer to the [Tweeteval official repository](https://github.com/cardiffnlp/tweeteval).

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
    print(f"{'-'*30}\n{text}")
    candidates = fill_mask(text)
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

## Example Feature Extraction 

```python
from transformers import AutoTokenizer, AutoModel, TFAutoModel
import numpy as np

MODEL = "cardiffnlp/twitter-roberta-base"
text = "Good night 😊"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

# Pytorch
encoded_input = tokenizer(text, return_tensors='pt')
model = AutoModel.from_pretrained(MODEL)
features = model(**encoded_input)
features = features[0].detach().cpu().numpy() 
features_mean = np.mean(features[0], axis=0) 
#features_max = np.max(features[0], axis=0)

# # Tensorflow
# encoded_input = tokenizer(text, return_tensors='tf')
# model = TFAutoModel.from_pretrained(MODEL)
# features = model(encoded_input)
# features = features[0].numpy()
# features_mean = np.mean(features[0], axis=0) 
# #features_max = np.max(features[0], axis=0)

```
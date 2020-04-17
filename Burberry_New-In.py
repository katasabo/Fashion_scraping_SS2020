from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
urls = [
    "https://us.burberry.com/womens-new-arrivals-new-in/",
    "https://us.burberry.com/womens-new-arrivals-new-in/?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
]

# SCRAPING & CREATING A LIST OF LINKS
doc = []
for url in urls:
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)

    for link in soup.find_all("a"):
        l = link.get("href")
        if "-p80" in l: # <-- THIS WILL NEED TO CHANGE
            doc.append(l)

# DEDUPLICATING THE LIST OF LINKS
doc_uniq = set(doc)
print("Number of unique items:"+str(len(doc_uniq)))

# CREATING A DICTIONARY WITH WORDS : COUNTS AND KEY : VALUE PAIRS
result = {}
for link in doc_uniq:
    words = link.replace("/", "").split("-")
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
            
words = list(result.keys())
counts = list(result.values())

# TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
df = pd.DataFrame.from_dict({
    "words": words,
    "counts": counts,
})

df_sorted = df.sort_values("counts", ascending = True)
df_rel = df_sorted[df_sorted['counts']>3]
print(df_rel.head())
print(df_rel.shape) 

# PLOTTING
plt.barh(df_rel['words'], df_rel['counts'], color = "#C19A6B")
plt.title("Most used words in Burberry 'New in' SS2020 Women collection")
plt.xticks(np.arange(0, 18, step=2))
plt.savefig("SS2020_Burberry_word_frequency.jpg")

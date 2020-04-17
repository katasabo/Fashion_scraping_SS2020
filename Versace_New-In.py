# VERSACE

# CREATING LIST OF RELEVANT URLS
url = "https://www.versace.com/us/en-us/women/new-arrivals/new-in/"
    
# SCRAPING & CREATING A LIST OF LINKS
doc = []
#for url in urls:
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc)
soup_f = soup.find_all("a")
for t in soup_f:
    a = t.get("href")
    if a.startswith("/us/en-us/women/new-arrivals/new-in/"):
        doc.append(a)


# DEDUPLICATING THE LIST OF LINKS
doc_uniq = set(doc)
print("Number of unique items:"+str(len(doc_uniq)))
#print(doc_uniq)

result = {}
garbage = []
for link in doc_uniq:
    if link.startswith("/us/en-us/women/new-arrivals/new-in/?"):
        continue
    words = link.replace("/us/en-us/women/new-arrivals/new-in/", "") .split("/")
    words = words[0].split("-")
    
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1

words = list(result.keys())
counts = list(result.values())
#print(result)

# TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
df = pd.DataFrame.from_dict({
    "words": words,
    "counts": counts,
})

df2 = df.set_index("words")
#df2 = df.drop(["a1008"],axis=0)
df_sorted = df2.sort_values("counts", ascending = True)
df_rel = df_sorted[df_sorted['counts']>2]
#print(df_rel.head())
#print(df_rel.shape) 

#PLOTTING
plt.barh(df_rel.index, df_rel['counts'], color = "#FFD700")
plt.title("Most used words in Versace 'New in' SS2020 Women collection")
plt.savefig("SS2020_Versace_word_frequency.jpg")

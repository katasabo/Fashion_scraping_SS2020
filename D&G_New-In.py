# CREATING LIST OF RELEVANT URLS
urls = []
#urls = list(urls)
for i in [1,2,3,4]:
    u = str("https://us.dolcegabbana.com/en/women/highlights/new-in/?page=") + str(i)
    urls.append(u)
    
#print(urls)

# SCRAPING & CREATING A LIST OF LINKS
doc = []
for url in urls:
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    soup_f = soup.find_all("a")
    
    for t in soup_f:
        a = t.get("aria-label")
        if a != None and a.startswith("Visit"):
            doc.append(a)
#print(doc)

# DEDUPLICATING THE LIST OF LINKS
doc_uniq = set(doc)
print("Number of unique items:"+str(len(doc_uniq)))

result = {}
for link in doc_uniq:
    words = link.replace("Visit", "").replace(" product page","").split(" ")                                                                                                                                      
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
del(result[""])
words = list(result.keys())
counts = list(result.values())

# TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
df = pd.DataFrame.from_dict({
    "words": words,
    "counts": counts,
})

df2 = df.set_index("words")
#df2.drop(["", "WITH"])
df_sorted = df2.sort_values("counts", ascending = True)
df_rel = df_sorted[df_sorted['counts']>4]
#print(df_rel.head())
#print(df_rel.shape) 

# PLOTTING
plt.barh(df_rel.index, df_rel['counts'], color = "#E0115F")
plt.title("Most used words in D&G 'New in' SS2020 Women collection")
plt.savefig("SS2020_D&G_word_frequency.jpg", pad_inches=0.1)

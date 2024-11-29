#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
import numpy as np 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import matplotlib.pyplot as plt
#%%
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('word_tockenize')
#nltk.download('punkt_tab')
#%%
df = pd.read_csv('linkedin_scrapping.csv')
#%%
skills_list = df['Requirements'].tolist()
additional_stopwords = ['experience', 'knowledge', 'skills', 'ability', 'required'
                        , 'preferred', 'must', 'plus', 'good', 'strong', 'excellent'
                        ,'degree','use','experienced','work','working','including'
                        ,'understanding','development','team','technical','years'
                        ,'years','background','field','related','industry'
                        ,'coursework','education','demonstrated','proficiency'
                        ,'student', 'preferably'
                        , 'using'
                        , 'e.g' , 'etc'
                        , 'familiarity','familiar', 'language', 'programming','languages'
                        ,'proficient' , 'advanced', 'basic'
                        , 'tools', 'techniques', 'methods', 'technologies', 'like'
                        , 'one', 'least', 'around'
                        ,'concepts', 'learn', 'new', 'improve', "large", 'environment', 'business'
                        , 'complex', 'quantitative', 'analytical', 'problems'
                        , 'systems', 'may', 'specific', 'specifically', 'across'
                       , 'similar'
                       ]
# Combine NLTK stopwords with additional stopwords
stop_words = set(stopwords.words('english')).union(set(additional_stopwords))
phrases_to_remove = ["data science", "data sets", "track record"]

 # from online dictionary and ngrams 
ds_terms = [
 "machine learning", "big data", "data management", "database management"
    , "relational database", "data warehousing", "statistical modeling", 'statistical analysis',
    "language model", 'large language models', 'language models', 'large language model', "ml", "llm",'llms', "generative model", 
    "data mining", "data analysis", "data visualization",
    "data engineering", "deep learning", "ai", 'regression analysis', 'linear regression'
    , "artificial intelligence", "natural language processing"
    , 'apache spark', "neural network", "computer vision",
    "etl", "supervised learning", "unsupervised learning",
    'web scraping', 'data cleaning', 'data preprocessing',
    'hypothesis testing', 'ab testing', 'time series analysis','experiment design'
    'predictive modeling', 'recommender system', 'data analysis', 'data analytics',
    'power bi', "marketing analytics", "business intelligence"
    , 'cloud computing', 'software engineering', 'software development'
    , 'statistical models', 'version control', 'git', 'causal inference'
    , 'problem solving', 'critical thinking', 'communication skills'   
    , 'answer business questions', 'decision making', 'business questions'
    , 'c', 'c++', 'hadoop', 
    'verbal communication', 'cross functional', 'cross functional teams'
    , 'amazon web services', 'google cloud', 'data modelling', 
    'data architecture', 'data governance', 'data quality', 'data integration'
    , 'complex data', 'structured data', 'unstructured data', 'semi-structured data'
    , 'team work', 'team player', 'team oriented', 'team environment'
    , 'quantitative analysis', 'qualitative analysis'
    , 'propensity score', 'nontechnical stakeholders', 'nontechnical teams', 'attention to detail'
    , 'difference in differences', 'fast-paced' , 'large datasets', 'large data sets'
    , 'business analysis', 'business analytics', 'busisness intelligence', 'training models'
    ,'distributed systems', 'parallel computing', 'scalable systems', 'scalable solutions'
    , 'production systems', 'data processing', 'operating systems', 'cross-functional teams'
    , 'virtue environment','product management', 'product development', 'product design'
    , 'models production', 'best practices', 'ml models', 'relational databases'
    ]
    

#%%
def preprocess_text(text, phrases=ds_terms):
    text = text.lower()
   
    phrases_to_remove = ["data science", "data sets", "track record"]
    for phrase in phrases_to_remove:
        text = text.replace(phrase, " ")
    text = re.sub(r'\.\s', ' ', text)
    #text = re.sub(r'\.$', '', text)
    text = re.sub(r'[^a-z0-9.\s]', '', text) 
    text = re.sub(r'(\b\w+)\s+(model|models)', r'\1_\2', text)
    text = re.sub(r'building\s+(\b\w+)', r'building_\1', text)
    #tokens = word_tokenize(text)
    for phrase in phrases:
        tokenized_phrase = "_".join(phrase.split())  # Convert to single token
        text = re.sub(rf'\b{re.escape(phrase)}\b', tokenized_phrase, text)

    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

#-----------------frequency -----------------------------------
# %%
from itertools import chain, combinations
from collections import Counter
skills_list_processed = [preprocess_text(skill, ds_terms) for skill in skills_list]
skills_list_reduced = [[token for token in skill if token not in ['data', '.' , 'models']] for skill in skills_list_processed]
skills_list_rep= [[token if token != ('ml' or 'ml_models' or 'machine_learning models') else 'machine_learning' for token in skills] for skills in skills_list_reduced]
skills_list_rep= [[token if token !='statistical' else 'statistics' for token in skills] for skills in skills_list_rep]
skills_list_rep= [[token if token !='analytics' else 'analysis' for token in skills] for skills in skills_list_rep]
skills_list_rep = [[token if token != ('cloud' or 'aws' or 'amazon web services') else 'cloud_computing' for token in skills] for skills in skills_list_rep]

all_skills = list(chain(*skills_list_rep))
skill_counts = Counter(all_skills)
essential_skills = skill_counts.most_common(40)  # Top 20 skills
print(essential_skills)

#%%
skill_counts_df = pd.DataFrame(skill_counts.items(), columns = ['skill','count'])
skill_counts_df = skill_counts_df.sort_values(by = 'count', ascending = False)
skill_counts_df.to_csv('skills_counts.csv', index=False)
#--------ngrams---------------------------------------------------
#%%
from nltk.util import ngrams
from nltk import FreqDist
all_tokens = [token for skill in skills_list_processed for token in skill]
# Generate N-grams (bigrams and trigrams)
bigrams = list(ngrams(all_tokens, 2))  # Bigrams
trigrams = list(ngrams(all_tokens, 3))  # Trigrams

########## Calculate frequency distributions
bigram_freq = FreqDist(bigrams)
trigram_freq = FreqDist(trigrams)

# Display most common phrases
print("Most Common Bigrams:")
for bigram, freq in bigram_freq.most_common(20):
    print(f"{' '.join(bigram)}: {freq}")

print("\nMost Common Trigrams:")
for trigram, freq in trigram_freq.most_common(20):
    print(f"{' '.join(trigram)}: {freq}")
#------word cloud--------------------------------------------------------
#%%
#word cloud 
from wordcloud import WordCloud
#skills_vis = [token for token in all_tokens if token not in ['data', '.', 'models']]
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(Counter(skill_counts))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Skills", fontsize=16)
plt.show()


#---network----------------------------------------------------------------------------------------
#%%
import networkx as nx
from itertools import combinations
from sklearn.cluster import SpectralClustering
#skills_list_network = [[token for token in skill if token not in ['data', '.']] for skill in skills_list_processed]
#skills_list_network_cleaned = [[token if token !='ml' else 'machine_learning' for token in skills] for skills in skills_list_network]
#skills_list_network_cleaned = [[token if token != ('ai' or 'llms') else 'artificial_intelligence' for token in skills] for skills in skills_list_network_cleaned]
#skills_list_network_cleaned = [[token if token != ('cloud' or 'aws' or 'amazon web services') else 'cloud_computing' for token in skills] for skills in skills_list_network_cleaned]
#networkskills= pd.read_csv('skills_counts.csv')
#node_importance = Counter([token for skills in skills_list_network_cleaned  for token in skills])
#important_nodes = [node for node, count in node_importance.items() if count > 14]
#skills_network = networkskills['skill'].tolist()[:19]
count_network = networkskills['count'].tolist()[:19]
filtered_skills_list = list(zip(skills_network, count_network))
#= [[token for token in skills if token in important_nodes]for skills in skills_list_network_cleaned]

#%%
# Add edges based on co-occurrence
G = nx.Graph()
#for skills in filtered_skills_list:
 #   for pair in combinations(skills, 2):
  #      G.add_edge(pair[0], pair[1])
edge_weights = Counter()

# Count co-occurrence weights
for skills in filtered_skills_list:
    for pair in combinations(skills, 2):
        edge_weights[pair] += 1

# Add edges with weights to the graph
for (node1, node2), weight in edge_weights.items():
    if weight > 7:
        G.add_edge(node1, node2, weight=weight)

# Create a filtered graph with only the edges between displayed nodes
filtered_graph = nx.Graph()

# Add only the nodes that are important
for node in skills_network:
    filtered_graph.add_node(node)

# Add edges only if both nodes are in the important nodes list
for (node1, node2) in G.edges():
    if node1 in important_nodes and node2 in important_nodes:
        filtered_graph.add_edge(node1, node2, weight=G[node1][node2]['weight'])
# Add node sizes based on importance (frequency)
node_sizes = [node_importance[node] * 200 for node in G.nodes()]

# Recompute adjacency matrix for the filtered graph
#adj_matrix_filtered = nx.to_numpy_array(filtered_graph)
# Perform spectral clustering
num_clusters = 2  # Set the number of clusters
adj_matrix = nx.to_numpy_array(G)  # Convert graph to adjacency matrix
clustering = SpectralClustering(n_clusters=num_clusters, affinity='precomputed', random_state=42)
labels = clustering.fit_predict(adj_matrix)

# Assign cluster labels to nodes
node_colors = [labels[list(filtered_graph.nodes()).index(node)] for node in G.nodes()]

# Draw the graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(filtered_graph, seed=42, weight='weight')
nx.draw_networkx_nodes(filtered_graph, pos, node_size=node_sizes, cmap=plt.cm.rainbow, node_color=node_colors)
nx.draw_networkx_edges(filtered_graph, pos, alpha=0.5, width=[filtered_graph[u][v]['weight'] for u, v in filtered_graph.edges()])
nx.draw_networkx_labels(filtered_graph, pos, font_size=10, font_color="black")

plt.title("Graph of Important Skills (Node Size = Importance)", fontsize=16)
plt.axis("off")
plt.show()

#----------------qualifications---------------------------------------------------------
#%%
# count the number of job that mention advanced degrees
# masters

qual= df['Qualification'].tolist()
masters = ['master', 'masters', 'ms', 'm.s', 'master of', 'graduate level', 'graduate degree']
count_master = df['Qualification'].str.lower().str.contains('|'.join(masters), na=False).sum()
print(f"Number of jobs that mention a Master's degree: {count_master}")
#49

#%%
bachelor = ['bachelor degree', 'bachelor', 'bs', 'b.s', 'bachelor of', 'undergraduate']
count_bach = df['Qualification'].str.lower().str.contains('|'.join(bachelor), na=False).sum()
print(f"Number of jobs that mention a bachekir's degree: {count_bach}")
#41


#%%
phd = ['phd', 'doctor of philosophy', 'doctorate']
count_phd = df['Qualification'].str.lower().str.contains('|'.join(phd), na=False).sum()
print(f"Number of jobs that mention a bachekir's degree: {count_phd}")

#30











# %%

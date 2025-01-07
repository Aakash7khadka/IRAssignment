search_results = [
    "Machine learning is a subset of artificial intelligence.",
    "Deep learning is a subset of machine learning.",
    "Artificial intelligence is transforming industries.",
    "Natural language processing is a key area in AI.",
    "Clustering is an unsupervised learning technique.",
    "K-means is a popular clustering algorithm.",
    "Supervised learning requires labeled data.",
    "Reinforcement learning is used in robotics.",
    "Data science involves statistics, machine learning, and programming.",
    "Big data technologies are essential for handling large datasets."
]

from sklearn.feature_extraction.text import TfidfVectorizer

# Convert text to TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(search_results)

from sklearn.cluster import KMeans

# Apply K-means clustering
num_clusters = 3  # You can adjust the number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Get cluster labels
cluster_labels = kmeans.labels_

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reduce dimensions to 2D using PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(X.toarray())

# Plot the clusters
plt.figure(figsize=(8, 6))
scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=cluster_labels, cmap='viridis', s=100)
plt.colorbar(scatter)
plt.title("Search Result Clustering")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
for i, txt in enumerate(search_results):
    plt.annotate(txt[:20], (reduced_data[i, 0], reduced_data[i, 1]), fontsize=8)
plt.show()
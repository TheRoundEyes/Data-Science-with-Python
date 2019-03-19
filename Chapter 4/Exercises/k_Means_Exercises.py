# Unsupervised Learning

# Exercise 2: Segmenting Iris into 2 Clusters using k-Means 

# import data
from sklearn import datasets
iris = datasets.load_iris()

# save the features as df
import pandas as pd
df = pd.DataFrame(iris.data)

# shuffle df
from sklearn.utils import shuffle
df_shuffled = shuffle(df, random_state=42)

# standardize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit scaler to the features
scaler.fit(df_shuffled)
# Transform features to scaled version
scaled_features = scaler.transform(df_shuffled)

# instantiate kmeans model
from sklearn.cluster import KMeans
model = KMeans(n_clusters=2)

# fit model
model.fit(scaled_features)

# get the cluster centroids
centroids = model.cluster_centers_ 
print(centroids)

# get the inertia
inertia = model.inertia_ 
print('The within-group sum of squares (i.e., inertia) with 2 clusters is {0:0.2f}'.format(inertia))

# get predicted labels
labels = model.labels_
print(labels)

# see how many of each label we have
import pandas as pd
pd.value_counts(labels)

# add label to df_shuffled
df_shuffled['Predicted_Cluster'] = labels
print(df_shuffled.head(5))

# clear kernel

###############################################################################

# Exercise 3: K-means clustering: Tuning n_clusters 

# import data
from sklearn import datasets
iris = datasets.load_iris()

# save the features as df
import pandas as pd
df = pd.DataFrame(iris.data)

# shuffle df
from sklearn.utils import shuffle
df_shuffled = shuffle(df, random_state=42)

# standardize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit scaler to the features
scaler.fit(df_shuffled)
# Transform features to scaled version
scaled_features = scaler.transform(df_shuffled)

# get inertia for every cluster
from sklearn.cluster import KMeans
inertia_list = []
for i in range(1, 11):
    # instantiate model
    model = KMeans(n_clusters=i)
    # fit model
    model.fit(scaled_features)
    # get inertia
    inertia = model.inertia_
    # append inertia to inertia_list
    inertia_list.append(inertia)
print(inertia_list)
    
# plot inertia by n_clusters
import matplotlib.pyplot as plt
x = list(range(1,11))
y = inertia_list
plt.plot(x, y)
plt.title('Inertia by n_clusters')
plt.xlabel('n_clusters')
plt.xticks(x)
plt.ylabel('Inertia')
plt.show()

# get the inertia values for 3
print('When n_clusters = 3, inertia = {:0.2f}'.format(y[2]))

# clear kernel

###############################################################################

# Exercise 4: tuning n_clusters using ensembles

# import data
from sklearn import datasets
iris = datasets.load_iris()

# save the features as df
import pandas as pd
df = pd.DataFrame(iris.data)

# shuffle df
from sklearn.utils import shuffle
df_shuffled = shuffle(df, random_state=42)

# standardize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit scaler to the features
scaler.fit(df_shuffled)
# Transform features to scaled version
scaled_features = scaler.transform(df_shuffled)

from sklearn.cluster import KMeans
import numpy as np
# create a list for the average inertia at each n_clusters
mean_inertia_list = []
# loop through n_clusters 1-10
for x in range(1, 11):
    # create a list for each individual inertia value at n_cluster
    inertia_list = []
    for i in range(100):
        # instantiate model
        model = KMeans(n_clusters=x)
        # fit model
        model.fit(scaled_features)
        # get inertia
        inertia = model.inertia_
        # append inertia to inertia_list
        inertia_list.append(inertia)
    # get mean of inertia list
    mean_inertia = np.mean(inertia_list)
    # append mean_inertia to mean_inertia_list
    mean_inertia_list.append(mean_inertia)
print(mean_inertia_list)    

# plot inertia by n_clusters
import matplotlib.pyplot as plt
x = list(range(1, len(mean_inertia_list)+1))
y = mean_inertia_list
plt.plot(x, y)
plt.title('Mean Inertia by n_clusters')
plt.xlabel('n_clusters')
plt.xticks(x)
plt.ylabel('Mean Inertia')
plt.show()

# get the inertia values for 3
print('When n_clusters = 3, inertia = {0:0.2f}'.format(y[2]))

"""
Without clearing the kernel, continue to the next section. 
We do not want to clear the kernel because we need to keep mean_inertia_list
in our environment, so we can plot inertia by n_clusters for original features
and PCA transformed features in the same plot
"""

# Exercise 5: Principal Component Analysis (PCA) with 2 Principal Components

# instantiate pca model
from sklearn.decomposition import PCA
# build model
model = PCA(n_components=2)

# fit model
model.fit(scaled_features)

# get explained variance ratio
explained_var_ratio = model.explained_variance_ratio_
print(explained_var_ratio)

# get the total explained variance with these 2 components
print('The total percentage of explained variance for the first 2 principal components is {0:0.2f}%'.format(sum(explained_var_ratio)*100))

# transform X into X_pca
df_pca = model.transform(scaled_features)

"""
Without clearing the kernel, continue to the next section. 
We do not want to clear the kernel because we need to keep mean_inertia_list
in our environment, so we can plot inertia by n_clusters for original features
and PCA transformed features in the same plot
"""

# Exerise 6: Principal Component Analysis: Tuning n_components

# instantiate pca model
from sklearn.decomposition import PCA
model = PCA()

# fit model
model.fit(scaled_features)

# transform into principle components
df_pca = model.transform(scaled_features)

# get the explained variance ratio for each component
explained_var_ratio = model.explained_variance_ratio_
print(explained_var_ratio)

# get the cumulative sum of explained variance by each component
import numpy as np
cum_sum_explained_var = np.cumsum(explained_var_ratio)
print(cum_sum_explained_var)

# set a threshold for % of variance in the data to preserve
threshold = .95
# programmatically check at which component we reach or surpass the threshold
for i in range(len(cum_sum_explained_var)):
    if cum_sum_explained_var[i] >= threshold:
        best_n_components = i+1
        break
    else:
        pass
print('The best n_components is {}'.format(best_n_components))

# plot cumulative explained variance by n_components
import matplotlib.pyplot as plt
x = list(range(1, len(explained_var_ratio)+1))
y = cum_sum_explained_var
plt.plot(x, y, color='blue', label='Explained Variance')
plt.title('{0} n_components are suggested to preserve {1} of the variance'.format(best_n_components, threshold))
plt.ylabel('Proportion of Explained Variance')
plt.xlabel('n_components')
plt.xticks(range(1, len(explained_var_ratio)+1))
plt.axhline(y=threshold, color='gray', linestyle='--', label = '{} Explained Variance'.format(threshold))
plt.legend(loc='best')
plt.show()

"""
Without clearing the kernel, continue to the next section. 
We do not want to clear the kernel because we need to keep mean_inertia_list
and best_n_components in our environment, so we can plot inertia by n_clusters 
for original features and PCA transformed features in the same plot
"""












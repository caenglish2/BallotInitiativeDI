#!/bin/python

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import numpy as np

data=pd.read_csv('data_train.csv')
data['clinton_margin']=data['CLINTON_%']-data['TRUMP_%']
max_income=data['PER_CAPITA_INCOME'].max()
data['PER_CAPITA_INCOME']=data['PER_CAPITA_INCOME']/max_income
X=data.ix[:,['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE','AFAMERPER','WHITESPER','ASIANPER','HISPANICPER','PERSENIORS','POVERTY_RATE','UNEMP_RATE','RURAL_POP','CITIZENS']]
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
#['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE','AFAMERPER','WHITESPER','ASIANPER','HISPANICPER','PERSENIORS','POVERTY_RATE','INCINEQUALITY','UNEMP_RATE','RURAL_POP','CITIZENS']
#X['nonwhite']=X['AFAMERPER']+X['ASIANPER']+X['HISPANICPER']

des=X.describe()
#print(des)
#print(X.head())
##print(kmeans.labels_)
#print(kmeans.cluster_centers_)

#print(data.head(100))
#print(X.head())

pca = PCA(n_components=2)
pca.fit(X)

#X['PCA1']=pca.transform(X)[:,0]
XPCA1=pca.transform(X)[:,0]
XPCA2=pca.transform(X)[:,1]
X_new=pca.transform(X)

X['PCA1']=XPCA1
X['PCA2']=XPCA2

def myplot(score,coeff,labels=['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE','AFAMERPER','WHITESPER','ASIANPER','HISPANICPER','PERSENIORS','POVERTY_RATE','UNEMP_RATE','RURAL_POP','CITIZENS']):
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    plt.scatter(xs * scalex,ys * scaley,s=1)
    for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')

#print(Y)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)
print(X.corr())
print(pca.components_)
myplot(X_new[:,0:2],np.transpose(pca.components_[0:2, :]))
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.show()

#corr.to_csv('corr.dat')

#print(Y[:100])
#plt.scatter(Y[:,0],Y[:,1])
#print(pca.explained_variance_ratio_) 

#plt.show()

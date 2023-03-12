'''python file'''

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


data = pd.read_csv('NetflixShows.csv', encoding = 'cp437')

del data['ratingLevel'], data['user rating size']

#Дроп дублей
df = data.drop_duplicates()


df['user rating score'] = df['user rating score'].replace('NaN', np.nan)
df_kmeans = df[['user rating score', 'release year']].copy()

#вот тут проблема - если писать isnull() - не на чем основывать предикт. 
#если писать notnull - нет кластеров для пустых значений

df_kmeans = df_kmeans[df_kmeans['user rating score'].notnull()]

X = df_kmeans[['release year']]


kmeans = KMeans(n_clusters = 5, random_state = 42)
kmeans.fit(X)

#Возможно тут я не то предикчу?
labels = kmeans.predict(X)


# При isnull в df_kmeans итут - df_means будет с пустыми значениями по нулям все 
#при notnull df_kmeans и тут- матрица предикта будет но ее не применить на пустые значения
#при несоотвествии isnull notnull - ошибка индексов
df.loc[df['user rating score'].notnull(), 'cluster'] = labels
df_means = df.groupby('cluster')['user rating score'].mean()
print(df_means)

#по идее тут должно заполнять пустые значения применив значения по кластеру по матрице но не заполняет изза ошибки выше
df.loc[df['user rating score'].isnull(), 'user rating score'] = df.loc[df['user rating score'].isnull(), 'cluster'].map(df_means)

#убираем лишнюю колонку
#df.dropna('cluster', axis=1, inplace = True)

print(df.tail(10))



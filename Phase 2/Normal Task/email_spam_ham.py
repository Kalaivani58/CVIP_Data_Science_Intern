# -*- coding: utf-8 -*-
"""Email Spam Ham.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15R-z9VrFit1UASfHNoVOdSpXoRyeFRr7

### ***IMPORT PACKAGES***
"""

import pandas as pd

"""### ***DATA EXPLORATION***"""

df = pd.read_csv('/content/spam.csv')
df

df.shape

df.size

df.columns

df.isna().sum()

"""### ***DATA PREPROCESSING***"""

df[df.duplicated(subset=['Category','Message'],keep=False)]

df.drop_duplicates(subset=['Category','Message'],keep='first',inplace=True)

df.info()

df.describe()

df['Category'].value_counts().to_frame()

df.loc[df['Category']=='spam','Category']=1
df.loc[df['Category']=='ham','Category']=0

df['Category']=df['Category'].astype('int64')

df.info()

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(4,5))
sns.countplot(data=df,x='Category')

"""### ***MODEL TRAINING AND TESTING***"""

x=df['Message']
y=df['Category']

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)
x_train.shape,x_test.shape,y_train.shape,y_test.shape

from sklearn.feature_extraction.text import TfidfVectorizer

fe=TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)
x_train_fe=fe.fit_transform(x_train)
x_test_fe=fe.transform(x_test)

from sklearn.linear_model import LogisticRegression

lr=LogisticRegression(max_iter=500)

lr.fit(x_train_fe,y_train)

lr.score(x_train_fe,y_train)

lr.score(x_test_fe,y_test)

y_pred=lr.predict(x_test_fe)

from sklearn.metrics import confusion_matrix,recall_score,precision_score,accuracy_score,f1_score,ConfusionMatrixDisplay

precision_score(y_test,y_pred)

accuracy_score(y_test,y_pred)

f1_score(y_test,y_pred)

cmd=ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,y_pred,labels=lr.classes_),display_labels=lr.classes_)
cmd.plot()

enter_your_mail=["My name is Pratik, and I'm part of a team that's passionate about making the tech community even better at Scaler."]

input_mail_features=fe.transform(enter_your_mail)
predict=lr.predict(input_mail_features)
if predict==1:
    print('mail is spam')
else:
    print('mail is not spam')
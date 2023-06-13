from flask import Flask, request, jsonify,render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
import re
import numpy as np
from  joblib import dump,load
import sklearn
import openai

# Download stopwords and lemmatizer data and punkt
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
openai.api_key = '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'

# Import your clustering model and any other necessary dependencies

app = Flask(__name__)


def chat_with_gpt(words):
    # Define the prompt and the system message
    text = f""" i want  of 5 social media pages or groups  or other virtual communities 
            that talk about topics related to this words {words}
                without description but mention if it is a group facebokk or etc
                                                                                    """
    prompt = "User: {}\nAI:".format(text)
    # Generate a chat response using the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the chatbot's reply
    chatbot_reply = response['choices'][0]['message']['content']
    return chatbot_reply



def extract_lines_with_numbers(text):
    lines_with_numbers = []
    lines = text.split('\n')

    for line in lines:
        if re.match(r'^\d', line):  # Check if the line starts with a digit
            lines_with_numbers.append(re.sub(r'^\d+.\s*', '', line))  # Remove the leading number

    return lines_with_numbers






def preprocess_text(text):
    
    if isinstance(text, float):
        return ""
    
    # Degits and Punctuation removal and lowercase
    text = re.sub(r"\d+", "", text)
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize text into words
    tokens = word_tokenize(text)

    # Remove stopwords
    additional_stopwords = list(set(['good','u','im','dr','berg','enough','use','want','thats','said','sometime','thank','see','much',
                                'go','find','make','one','day','think','month','year','maybe','week','youre',"going","make","thing",
                                'especially','u','mean','hour','almost','used','ect','look','dont','doesnt','may',"etc","told","another",
                                'easy','right','well','give','age','cant','lot','ive','love','still','dr berg',"last",'amazing',"didnt",
                                'end','many','went','know','take','come','say','come','gon na','time','video','done',"alway",'little','hi',
                                'hour','true','year','ago','become','man','even','isnt','people','everything','literally','without','keto',
                                'really','thanks','made','seem',"got","ate","let",'getting','add','pretty','year','old','watch','ok','least',
                                'found','never','thought','le','put','idea',"hard","every",'starting',"keep","person",'feeling',"someone", "god",
                                'day','bad','guy','trying','started','understand','new','anuone',"able",'lol','due',"big",'live',"two",       
                                'month','gon','na','sometimes','best',"happy","least",'felt','daily','hole','last',"amazing",'definitely',
                                "tried",'part','hope','long','fast','please','half','kind',"important",'reason',"instead",'stuff','great',
                                'making','away','today','using','tell','told','week','normal','something','feel',"month",'day','year','years'
                                ,'actually','added',"already",'also','always','amount',"anyone",'anything','around',"appreciate",'different'
                                ,'bit',"bp","bro",'gave','lb',"need",'like','oat',"get",'help','pm','stop']))

    stop_words = set(stopwords.words('english'))
    stop_words.update(additional_stopwords )
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    tokens = [lemmatizer.lemmatize(word,pos="v") for word in tokens]

    
    # Join tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text




def predict(my_text,tfidf_vect,kmeans,total):
    preprocessed_text = preprocess_text(my_text)
    text_vector = tfidf_vect.transform([preprocessed_text])
    predicted_cluster = kmeans.predict(text_vector)

    return int(predicted_cluster)




def return_topics(tfidf_vect,kmeans,predicted_cluster):

    feature_names = tfidf_vect.get_feature_names_out()
    centroids = kmeans.cluster_centers_
    cluster_topics = []

    for i, centroid in enumerate(centroids):
        top_indices = centroid.argsort()[-5:][::-1]
        cluster_topics.append([feature_names[ind] for ind in top_indices])

    topics=cluster_topics[predicted_cluster] 
    return topics   
    


def return_comments(my_text,tfidf_vect,kmeans,total):
    predicted_cluster=predict(my_text,tfidf_vect,kmeans,total)
    comments=total[total['cluster']==predicted_cluster]['comment'].sample(n=5).values

    return comments



# Define a route for clustering comments

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/process_comments', methods=['POST'])
def cluster_comments():
    # Get the comments from the request
    my_text = request.form.get('comments')
    print(my_text)


    tfidf_vect=load("tfidf_vect")
    kmeans=load("kmeans")
    total=pd.read_csv("./my_final_data.csv")


    cluster_number=predict(my_text,tfidf_vect,kmeans,total)

    topics=return_topics(tfidf_vect,kmeans,cluster_number)
    response=chat_with_gpt(topics)
    links=extract_lines_with_numbers(response)

    comments=return_comments(my_text,tfidf_vect,kmeans,total)

    return render_template('results.html', cluster_number=cluster_number, comments=comments,links=links)
    




if __name__ == '__main__':
    app.run()

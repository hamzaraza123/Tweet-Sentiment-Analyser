import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Create the main application window
app = tk.Tk()
app.title("TWEET SENTIMENT ANALYSIS")
app.geometry("655x580")

# Create a canvas for the background image
canvas = tk.Canvas(app, width=3900, height=3000)
canvas.pack()

# Load the background image (replace 'X.png' with your image path)
background_image = tk.PhotoImage(file='C:/Users/ACER/Desktop/VS CODES/X.png')
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Label and Entry for entering a tweet
tweet_label = tk.Label(app, text="ENTER TWEET:", bg="lightblue")
tweet_label.place(x=390, y=240)

tweet_entry = tk.Entry(app, width=17)
tweet_entry.place(x=377, y=265)

# Function for tweet preprocessing
def preprocess_tweet(tweet):
    # Remove special characters and symbols
    tweet = re.sub(r'[^\w\s]', '', tweet)
    
    # Convert to lowercase
    tweet = tweet.lower()
    
    # Remove URLs
    tweet = re.sub(r'http\S+', '', tweet)
    
    # Remove numbers
    tweet = re.sub(r'\d+', '', tweet)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
    tweet = ' '.join([word for word in word_tokens if word not in stop_words])
    
    # Remove extra white spaces
    tweet = ' '.join(tweet.split())
    
    return tweet

# Function to perform sentiment analysis
def perform_sentiment_analysis(tweet):
    tweet = preprocess_tweet(tweet)
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Function to display sentiment analysis result
def search():
    tweet = tweet_entry.get()
    sentiment = perform_sentiment_analysis(tweet)
    sentiment_result = f'YOUR TWEET IS: {sentiment}'

    # Update the result label
    result_label.config(text=sentiment_result)

# Button to trigger sentiment analysis
generate_button = tk.Button(app, text="GENERATE!", bg="lightgreen", command=search)
generate_button.place(x=397, y=303)

# Label to display sentiment analysis result
result_label = tk.Label(app, text="SENTIMENT IS: ", bg="lightblue")
result_label.place(x=140, y=355)


# Label and Entry for entering a tweet
tweet_label = tk.Label(app, text="UPLOAD A CSV FILE:", bg="lightblue")
tweet_label.place(x=155, y=240)

file_path_entry = tk.Entry(app, width=17)
file_path_entry.place(x=160, y=265)

# Function for uploading a CSV file
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

upload_button = tk.Button(app, text="BROWSE", bg="lightblue", command=upload_file)
upload_button.place(x=185, y=290)

# Function for sentiment analysis
def analyze_sentiments():
    file_path = file_path_entry.get()
    if not file_path:
        result_label.config(text="Please upload a CSV file first.")
        return
    
    try:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path)

        # Define a function for text cleaning
        def clean_text(text):
    
            # Remove special characters and symbols
            text = re.sub(r'[^\w\s]', '', text)

            # Convert to lowercase
            text = text.lower()

            # Remove URLs
            text = re.sub(r'http\S+', '', text)

            # Remove numbers
            text = re.sub(r'\d+', '', text)

            # Remove stop words
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(text)
            text = ' '.join([word for word in word_tokens if word not in stop_words])

            # Remove extra white spaces
            text = ' '.join(text.split())

            return text


        # Apply the cleaning function to the 'content' column
        data['content'] = data['content'].apply(clean_text)

        # Function to perform sentiment analysis
        def perform_sentiment_analysis(tweet):
            tweet = preprocess_tweet(tweet)
            analysis = TextBlob(tweet)
            polarity = analysis.sentiment.polarity

            if polarity > 0:
                return 'Positive'
            elif polarity < 0:
                return 'Negative'
            else:
                return 'Neutral'


        # Apply the sentiment analysis function to the 'content' column
        data['sentiment'] = data['content'].apply(perform_sentiment_analysis)

        # Calculate the percentages
        sentiment_counts = data['sentiment'].value_counts(normalize=True) * 100

        # Display the sentiment percentages
        result_label1=tk.Label(app, text=f"Positive Sentiment: {sentiment_counts.get('Positive', 0):.2f}%", bg="lightblue").place(x=138, y=385)
        result_label2=tk.Label(app,text=f"Negative Sentiment: {sentiment_counts.get('Negative', 0):.2f}%", bg="lightblue").place(x=138, y=395)
        result_label3=tk.Label(app,text=f"Neutral Sentiment: {sentiment_counts.get('Neutral', 0):.2f}%", bg="lightblue").place(x=138, y=405)
   
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Button to trigger sentiment analysis
generate_button = tk.Button(app, text="GENERATE!", bg="lightgreen", command=analyze_sentiments)
generate_button.place(x=178, y=323)

# Label to display sentiment analysis result
result_label = tk.Label(app, text="SENTIMENT IS: ", bg="lightblue")
result_label.place(x=360, y=355)

# Start the GUI main loop
app.mainloop()
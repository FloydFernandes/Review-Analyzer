from flask import Flask, render_template, request, redirect, url_for
import review_scraper as rs
import text_analyzer


app = Flask(__name__)

@app.route('/')
def home_page():

    return render_template("multiple_user.html")

analysis = {}

@app.route('/features', methods=['GET', 'POST'])
def features():
    global analysis
    if request.method == "POST":
        try:
            if request.form["review-link"] == "":
                return render_template("error.html")
            else:
                page = request.form["review-link"]

            # Product name:
                get_name = page.split("/")
                product_name = get_name[3]
                analysis["product_name"] = product_name

                data = rs.get_df(page)
                data_len = len(data["Review_content"])
                
                analysis["data_len"] = data_len

                data["cleaned_review"] = data["Review_content"].apply(lambda x: text_analyzer.text_cleaner(x))
                


                sentiment_data = text_analyzer.sentiment_analysis(data)

                pos_rev_count = text_analyzer.get_positive(sentiment_data)
                neg_rev_count = text_analyzer.get_negative(sentiment_data)
                neu_rev_count = text_analyzer.get_neutral(sentiment_data)
                analysis["pos_count"] = pos_rev_count 
                analysis["neg_count"] = neg_rev_count 
                analysis["neu_count"] = neu_rev_count 
                


                avg_rating = text_analyzer.avg_rating(data)
                analysis["avg_rating"] = avg_rating 


                rating = data["Rating"].value_counts()
                analysis["rating"] = rating

                emotion_data = text_analyzer.emotion_mining(data)


                names_of_reviewers = [x["Name"] for x in emotion_data]
                analysis["names_of_reviewers"] = names_of_reviewers



                sad = [x["Sad"] for x in emotion_data]
                angry = [x["Angry"] for x in emotion_data]
                happy = [x["Happy"] for x in emotion_data]
                surprise = [x["Surprise"] for x in emotion_data] 
                fear = [x["Fear"] for x in emotion_data]
                analysis["sad"] = sad
                analysis["angry"] = angry
                analysis["happy"] = happy
                analysis["surprise"] =surprise
                analysis["fear"] = fear


                pos_list = text_analyzer.lemma_words_para(data[data['Rating'] > 3])
                analysis["pos_list"] = pos_list


                neg_list = text_analyzer.lemma_words_para(data[data['Rating'] < 3])
                neu_list= text_analyzer.lemma_words_para(data[data['Sentiment_VADER'] == 'Neutral'])
                analysis["neg_list"] = neg_list
                analysis["neu_list"] = neu_list


                rating_counter = text_analyzer.rating_value_counter(data)
                analysis["rating_counter"] = rating_counter


                extreme_sent = text_analyzer.extreme_sentiments(data)
                analysis["extreme_sent"] = extreme_sent

                ner_pos_data = text_analyzer.ner_analysis(data.loc[(data['Rating'] >= 4)])
                ner_pos_labels = [x[0] for x in ner_pos_data]
                ner_pos_val = [x[1] for x in ner_pos_data]
                analysis["ner_pos_labels"] = ner_pos_labels
                analysis["ner_pos_val"] = ner_pos_val

                try:
                    ner_neu_data = text_analyzer.ner_analysis(data.loc[(data['Rating'] == 3)])
                    ner_neu_labels = [x[0] for x in ner_neu_data]
                    ner_neu_val = [x[1] for x in ner_neu_data]
                    analysis["ner_neu_labels"] = ner_neu_labels
                    analysis["ner_neu_val"] = ner_neu_val
                except:
                    ner_neu_data = text_analyzer.ner_analysis(sentiment_data.loc[(sentiment_data["Sentiment_VADER"] == "Neutral")])
                    ner_neu_labels = [x[0] for x in ner_neu_data]
                    ner_neu_val = [x[1] for x in ner_neu_data]
                    analysis["ner_neu_labels"] = ner_neu_labels
                    analysis["ner_neu_val"] = ner_neu_val

                ner_neg_data = text_analyzer.ner_analysis(data.loc[(data['Rating'] < 3)])
                ner_neg_labels = [x[0] for x in ner_neg_data]
                ner_neg_val = [x[1] for x in ner_neg_data]
                analysis["ner_neg_labels"] = ner_neg_labels
                analysis["ner_neg_val"] = ner_neg_val

                ngram_pos_data = text_analyzer.ngram_words(data.loc[(data['Rating'] > 3)], 2, 3)
                ngram_pos_labels = [x[0] for x in ngram_pos_data]
                ngram_pos_val = [x[1] for x in ngram_pos_data]
                analysis["ngram_pos_labels"] = ngram_pos_labels
                analysis["ngram_pos_val"] = ngram_pos_val

                try:
                    ngram_neu_data = text_analyzer.ngram_words(data.loc[(data['Rating'] == 3)], 2, 3)
                    ngram_neu_labels = [x[0] for x in ngram_neu_data]
                    ngram_neu_val = [x[1] for x in ngram_neu_data]
                    analysis["ngram_neu_labels"] = ngram_neu_labels
                    analysis["ngram_neu_val"] = ngram_neu_val
                except:
                    ngram_neu_data = text_analyzer.ngram_words(sentiment_data.loc[(sentiment_data["Sentiment_VADER"] == "Neutral")], 2, 3)
                    ngram_neu_labels = [x[0] for x in ngram_neu_data]
                    ngram_neu_val = [x[1] for x in ngram_neu_data]
                    analysis["ngram_neu_labels"] = ngram_neu_labels
                    analysis["ngram_neu_val"] = ngram_neu_val

                ngram_neg_data = text_analyzer.ngram_words(data.loc[(data['Rating'] < 3)], 2, 3)
                ngram_neg_labels = [x[0] for x in ngram_neg_data]
                ngram_neg_val = [x[1] for x in ngram_neg_data]
                analysis["ngram_neg_labels"] = ngram_neg_labels
                analysis["ngram_neg_val"] = ngram_neg_val


                date_data = text_analyzer.date_analyzer(data)
                analysis["date_data"] = date_data


                return render_template("features_multiple.html", prod_name = analysis["product_name"])


        except:
            return render_template("error.html")


@app.route('/rating_analysis')
def rating_analysis():
    global analysis

    product_name = analysis["product_name"]

    data_len = analysis["data_len"]
                


    pos_rev_count = analysis["pos_count"]
    neg_rev_count = analysis["neg_count"]
    neu_rev_count = analysis["neu_count"]

                


    avg_rating = analysis["avg_rating"]


    rating = analysis["rating"]

    features = {"Number of reviews (limit 100)":data_len,"Number of positive reviews":pos_rev_count,
    "Number of neutral reviews":neu_rev_count, "Number of negative reviews":neg_rev_count,
    "Average rating":avg_rating}


    rating_counter = analysis["rating_counter"]

    date_data = analysis["date_data"]

    return render_template("rating_analysis.html",
    features=features, prod_name = product_name,
    ratings= rating, ratings_count = rating_counter, date=date_data)


@app.route('/sentiment_analysis')
def sentiment_analysis():
    global analysis

    product_name = analysis["product_name"]

    names_of_reviewers = analysis["names_of_reviewers"]


    sad = analysis["sad"]
    angry = analysis["angry"]
    happy = analysis["happy"]
    surprise = analysis["surprise"]
    fear = analysis["fear"]


    extreme_sent = analysis["extreme_sent"]

    return render_template("sentiment_analysis.html", 
    names_cust = names_of_reviewers, 
    sad=sad, 
    happy=happy, 
    angry=angry, 
    surprise=surprise, 
    fear=fear,
    prod_name = product_name,
    extreme = extreme_sent)



def single_none():
    single_sentiment_null = {"neg": 0, "neu": 0, "pos": 0, "compound": 0}
    single_emotion_null = {"Happy": 0, "Angry": 0, "Sad": 0, "Surprise": 0, "Fear": 0}

    return [single_sentiment_null, single_emotion_null]

@app.route('/single_user')
def single_user():
    single_none_data = single_none() 
    single_sentiment_null = single_none_data[0]

    single_emotion_null = single_none_data[1]

    return render_template("single_user.html", sentiment = single_sentiment_null,
            emotion = single_emotion_null)


@app.route('/features_single', methods=['GET', 'POST'])
def single_user_features():

    single_none_data = single_none() 
    single_sentiment_null = single_none_data[0]

    single_emotion_null = single_none_data[1]

    if request.method == "POST":
        if request.form["user-text"] == "":

            render_template("single_user.html", sentiment = single_sentiment_null,
            emotion = single_emotion_null)

        else:    
            text = request.form["user-text"]
            
            single_sentiment = text_analyzer.single_sentiment_analyzer(text)

            single_emotion = text_analyzer.single_emotion_analyzer(text)

            single_sent_blob = text_analyzer.single_sentiment_blob(text)
            print(single_sent_blob)

            

            return render_template("single_user.html", sentiment = single_sentiment,
            emotion = single_emotion, text=text)

    return render_template("single_user.html", sentiment = single_sentiment_null,
    emotion = single_emotion_null)

@app.route('/ner')
def ner():
    global analysis
    ner_pos_labels = analysis["ner_pos_labels"]
    ner_pos_val = analysis["ner_pos_val"]

    ner_neu_labels = analysis["ner_neu_labels"]
    ner_neu_val = analysis["ner_neu_val"]

    ner_neg_labels = analysis["ner_neg_labels"]
    ner_neg_val = analysis["ner_neg_val"] 

    ngram_pos_labels = analysis["ngram_pos_labels"]
    ngram_pos_val = analysis["ngram_pos_val"]

    ngram_neu_labels = analysis["ngram_neu_labels"]
    ngram_neu_val = analysis["ngram_neu_val"]

    ngram_neg_labels = analysis["ngram_neg_labels"]
    ngram_neg_val = analysis["ngram_neg_val"]

    return render_template("ner.html", 
    ner_pos_keys = ner_pos_labels,
    ner_pos_values = ner_pos_val,
    ner_neu_keys = ner_neu_labels,
    ner_neu_values = ner_neu_val,
    ner_neg_keys = ner_neg_labels,
    ner_neg_values = ner_neg_val,
    ngram_pos_keys = ngram_pos_labels,
    ngram_pos_values = ngram_pos_val,
    ngram_neu_keys = ngram_neu_labels,
    ngram_neu_values = ngram_neu_val,
    ngram_neg_keys = ngram_neg_labels,
    ngram_neg_values = ngram_neg_val
    )


@app.route('/wordcloud')
def word_cloud():
    global analysis
    pos_list = analysis["pos_list"]
    neg_list = analysis["neg_list"]
    neu_list= analysis["neu_list"]

    return render_template("wordcloud.html",
    pos_words=pos_list[0], pos_vals = pos_list[1],
    neg_words= neg_list[0], neg_vals = neg_list[1],
    neu_words= neu_list[0], neu_vals = neu_list[1],)



@app.route('/about')
def about_page():
    return render_template("about.html")
    





if __name__ == "__main__":
    app.run(debug=False)
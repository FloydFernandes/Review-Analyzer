from bs4 import BeautifulSoup as bs
import requests
import pandas as pd




def get_df(page):

    names_list = []
    review_titles_list = []
    rating_list = []
    date_list = []
    review_list = []

    retry = 0

    page_number = 1

    page_available = True

    iterations = 1

    while page_available and len(names_list) <= 100:
    
        if page_number < 2:
            soup = getlink(page, page_number="")
        
        # Names
            names = get_items(soup, "span", "a-profile-name")
            names = names[2:]

        # Titles
            review_titles = get_items(soup, "a", html_class= "review-title")

        
            if 10 > len(review_titles) > 0:
                review_titles = get_items(soup, "span", hover_tag={"data-hook":"review-title"})
        

            
        # Rating
            rating = get_items(soup, "i", "review-rating")
            rating = rating[2:]
        
        # Date
            dates = get_items(soup, "span", "review-date")
            dates = dates[2:]
        
        # Review_content
            reviews = get_items(soup, "span", hover_tag={"data-hook": "review-body"})

        
            if len(names) == 0 or len(review_titles) == 0 or len(reviews) == 0:
                if len(names) == 0:
                    if len(review_titles) > 0:
                        review_titles = []
                    if len(reviews) > 0:
                        reviews = []
                if len(review_titles) == 0:
                    if len(names) > 0:
                        names = []
                    if len(reviews) > 0 :
                        reviews = []
                if len(reviews) == 0:
                    if len(names) > 0:
                        names = []
                    if len(review_titles) > 0:
                        review_titles = []
                    

                retry += 1
                if retry < 10:
                    continue
                else:
                    break
            else:
                page_number += 1

    
                for i in range(len(names)):
                    names_list.append(names[i].get_text())
                    review_titles_list.append(review_titles[i].get_text().strip("\n"))
                    rating_list.append(rating[i].get_text())
                    date_list.append(dates[i].get_text())
                    review_list.append(reviews[i].get_text().strip("\n"))
            

        else:
            soup = getlink(page, page_number)
        
        # Names
            names = get_items(soup, "span", "a-profile-name")
        
        # To get get out of loop when pages are over
            if len(names) == 2:
                page_available = False
            
            names = names[2:]


            # Titles
            review_titles = get_items(soup, "a", hover_tag={"data-hook":"review-title"})
        
              

            if 10 > len(review_titles) > 0:
                review_titles_foreign = get_items(soup, "span", hover_tag={"data-hook":"review-title"})
                review_titles_foreign = review_titles_foreign[2:] 
                for x in review_titles_foreign:
                    review_titles.append(x)

        
                        
        # rating
            rating = get_items(soup, "i", "review-rating")
            rating = rating[2:]
        
        # Date
            dates = get_items(soup, "span", "review-date")
            dates = dates[2:]
        
        # Review_content
            reviews = get_items(soup, "span", hover_tag={"data-hook": "review-body"})

        
            if len(names) == 0 or len(review_titles) == 0 or len(reviews) == 0:
                if len(names) == 0:
                    if len(review_titles) > 0:
                        review_titles.pop()
                    if len(reviews) > 0:
                        reviews.pop()
                
                if len(review_titles) == 0:
                    if len(names) > 0:
                        names.pop()
                    if len(reviews) > 0 :
                        reviews.pop()

                if len(reviews) == 0:
                    if len(names) > 0:
                        names.pop()
                    if len(review_titles) > 0:
                        review_titles.pop()
                    
                retry+=1
                if retry < 10:
                    continue
                else:
                    break
            
            else:
                page_number += 1
            
        
            for i in range(len(names)):
                names_list.append(names[i].get_text())
                review_titles_list.append(review_titles[i].get_text().strip("\n"))
                rating_list.append(rating[i].get_text())
                date_list.append(dates[i].get_text())
                review_list.append(reviews[i].get_text().strip("\n"))

        
        
        iterations += 1
        
        

    rating_float_list = []
    for x in rating_list:
        rating_float_list.append(float(x[:4]))


    data = {"Name": names_list, "Review_Title": review_titles_list, "Rating": rating_float_list, "Date": date_list, "Review_content": review_list}
    # Change name of Dataframe 
    df = pd.DataFrame(data)

    return df




def getlink(page, page_number=""):
    '''Connection with the page'''
    if page_number != "":
        link = f"{page}&pageNumber={page_number}"
        connection = requests.get(link)
        soup = bs(connection.content, "html.parser")
        return soup
    else:
        connection = requests.get(page)
        soup = bs(connection.content, "html.parser")
        return soup



def get_items(connection, tag="", html_class="", hover_tag=""):
    '''Getting a list of items called'''
    if html_class != "":
        the_list = connection.find_all(tag, class_= html_class)
    else:
        the_list = connection.find_all(tag, hover_tag)
    return the_list









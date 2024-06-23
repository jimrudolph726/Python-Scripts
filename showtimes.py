import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
import time
import sys

# create variables
today = date.today()
today_string = today.strftime("%Y%m%d")
data = []

#define figure and axes
fig, ax = plt.subplots()

#hide the axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

def generate_dataframe(soup):
    # Find the movie blocks
    movie_blocks = soup.find_all("div", class_=f"black-box new-red-box hr-line schedule-dates date-{today_string}")
    if not movie_blocks:
        print("no showtimes for current day")
        quit()
    # Iterate through each movie block
    for movie_block in movie_blocks:
        
        # get movie title
        title_element = movie_block.find("h3")
        movie_title = title_element.text.strip()

        # get showtimes
        future_times = []
        showtime_elements = movie_block.find_all("li", class_="black-btns")
        showtimes = [showtime.a.text.strip() for showtime in showtime_elements]
        showtimes_clean = list(OrderedDict.fromkeys(showtimes))
        current_time = datetime.now().time()
        formatted_time = current_time.strftime("%I:%M %p")

        # format showtimes_clean and extract latest showtime
        datetime_format = "%I:%M %p"
        datetime_list = [datetime.strptime(time, datetime_format) for time in showtimes_clean]
        latest_showtime = max(datetime_list).time()
        # strip 0 from from of time if applicable
        if formatted_time[0] == '0':
            formatted_time = formatted_time[1:]
        
        # add all showtimes if current time is still AM
        if formatted_time[-2] == 'A':
            future_times = showtimes_clean
        # otherwise, only add showtimes that are later than current time
        elif current_time < latest_showtime:
            future_times = [time for time in showtimes_clean if time > formatted_time]
        else:
            future_times = ['No more showtimes for today']
 
        # strip brackets from list elements
        data.append((movie_title, '   '.join(future_times)))
    
    # store movie title and showtimes in list
    # create matplotlib table
    df = pd.DataFrame(data, columns=["Movie Title", "Showtimes"])
    
    return df

def fetch_url(url):
    retries = 0
    while retries < 3:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
            retries += 1
            if retries < 3:
                print(f"Retrying... (Attempt {retries}/3)")
                time.sleep(2)  # Add a small delay before retrying
    print(f"Failed to fetch URL after 3 attempts.")
    sys.exit(1)

def main():
    url = "https://manntheatres.com/theatre/89/Edina-4"
    response = fetch_url(url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        df = generate_dataframe(soup)
    except Exception as e:
        print(f"An error occurred while generating the dataframe: {e}")
        sys.exit(1)
        
    # create table of movie titles and showtimes
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    # Set the size of the figure to make the window bigger
    fig.set_size_inches(10, 4)  # Adjust the width and height as needed
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

#! /usr/bin/python3

# using request for all cool HTTP requests
import requests

# using BeautifulSoup for an HTML parser
from bs4 import BeautifulSoup

from datetime import datetime
import timeit

# main process
def main():

    # start timer
    start = timeit.default_timer()

    """ opens CSV file to write to
        the CSV is formatted as such:
        lineID, characterID, board, text
    """
    filename = datetime.now().time().strftime('%Y-%m-%d-%H-%M') + '.csv'
    out = open('out/' + filename, 'w')

    # request main page
    r = requests.get('http://www.4chan.org/')
    soup = BeautifulSoup(r.text, 'html.parser')

    # gets a list of boards from the main page
    boardlist = soup.find_all('a', 'boardlink')

    # loops through the board list getting the links
    for board in boardlist:
        link = board.get('href')

        # if the link is a valid board, then it will start scraping it
        if(not (len(link) > len('//boards.4chan.org/****/'))):
            r = requests.get('http:' + link)

    # stop timer
    stop = timeit.default_timer()

    print('Time Program took in seconds: ' + str(stop - start) + 's')

def scrape(link):


if __name__ == "__main__":
    main()

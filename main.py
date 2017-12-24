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
            scrape(link, out)

    # stop timer and print results
    stop = timeit.default_timer()
    print('Time Program took in seconds: ' + str(stop - start) + 's')

def scrape(link, out):
    # make a list of threads, then scrape
    # class thread is for each thread
    # link to each thread is `link` + thread/id
    links = []

    # a list of all images on the thread
    imgs = []

    # will go for all pages in each board
    for i in range(10):
        post = ''
        if i != 0:
            post = str(i + 1) + '/'
        out_link = link + post
        r = requests.get('http:' + out_link)
        soup = BeautifulSoup(r.text, 'html.parser')
        for thread in soup.find_all('div', 'thread'):
            t_id = thread.get('id')
            links.append('http:' + out_link + 'thread/' + t_id[1:])
            out.write('http:' + out_link + 'thread/' + t_id[1:] + '\n')

        # scrapes all image links
        for img in soup.find_all('a'):
            if img.get('href').endswith(('jpg', 'png')):
                imgs.append('http:' + img.get('href'))

        # writes all images to disk
        for img in imgs:
            r = requests.get(img, stream=True)
            if r.status_code == 200:
                path = './out/media/' + img.replace('/', '')
                with open(path, 'wb') as f:
                    print('writing to: ' + path)
                    for chunk in r:
                        f.write(chunk)
                print('done with that file (^^)b')

# runs main function
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:23:14 2020

@author: ThachLN
Home page: https://thachln.github.io
"""
import os
import pandas as pd
from lxml import html
import requests
from pathlib import Path


df = pd.read_csv('https://thachln.github.io/datasets/Springer_Ebooks.csv')
df.shape
nBook = df.shape[0]

# =============================================================================
# This function gets pdf link download.
# url: Link of book
# =============================================================================
def getDownloadLink(url):
    rootUrl = 'http://link.springer.com'

    page = requests.get(url)

    # convert the data received into searchable HTML
    extractedHtml = html.fromstring(page.content)

    # use an XPath query to find the image link (the 'src' attribute of the 'img' tag).
    pdfLink = extractedHtml.xpath("//a[@title='Download this book in PDF format']/@href") # in our example, result = ‘/images/GrokkingAlgorithms.jpg’

    downloadLink = rootUrl + pdfLink[0]
    
    return downloadLink     

# Change your folder to contains books
    
outFolder = 'D:/Books/SpringerLink/'
# Create root folder
if (not os.path.exists(outFolder)):
        os.mkdir(outFolder)
        
# Scan all data frame of free books
for index, row in df.iterrows():
    url = row['OpenURL']
    title = row['Book Title']
    
    # Create folder
    bookFolderPath = os.path.join(outFolder, title)
    if (not os.path.exists(bookFolderPath)):
        os.mkdir(bookFolderPath)
    
    # Build path to store content of book
    filePdfPath = os.path.join(bookFolderPath, title + ".pdf")
    if (not os.path.exists(filePdfPath)):
        filename = Path(filePdfPath)
        
        # Download book and write to path
        print(f"Dowloading book {index + 1}/{nBook}, '{title}'")
        downloadLink = getDownloadLink(url)
        response = requests.get(downloadLink)
        filename.write_bytes(response.content)
    else:
        print("Book is exited.")
    # Uncomment these command to dowload all books from the data frame.
    if index > 3:
        break


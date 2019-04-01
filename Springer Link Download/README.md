# Introducion

This is a software named Springer Link Download (SLD). SLD is able to download articles using only a list of links from the Springer Website in .csv format.

To do this, it performs the following functions:

1. It receives as input a .CSV file; 
2. The algorithm reads the list and fetches all abstracts;
3. Validate an article if there is any match between the String and the abstract.
4. Save list of validated articles;
5. Download the articles in the software folder.


# Installing

You can install SLD:

    $ pip3 install -r requirements.txt

# Dependencies

* This project uses version 3 of Python with the libraries: wget, requests, bs4, pandas and numpy.

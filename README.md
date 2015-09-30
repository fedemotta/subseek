# Subseek
Search subtitles for all your movies and series with a single command line script

[![PyPI version](https://badge.fury.io/py/subseek.svg)](http://badge.fury.io/py/subseek)

## Description
Subseek is a Python script which list all your local movies and series and search 
subtitles for them. The web search is done using different subtitle providers 
(currently Subdivx only) and different search engine providers (Google and DuckDuckGo).
It uses the file and path name with an algorithm which made several changes to the searched 
text to find the best match. You can search, in example, subtitles for all the seasons of 
a complete TV show, a couple of movies and the last episode of your favorite TV show in a 
single command line script.

## Installation
```
pip install -r requirements.txt

```

## Usage
```
python -m subseek -p (path) [option]

Options and arguments:
----------------------
-p path      : String. Required. Root path to start the process; 
               also --path=path. 
               Example: python console.py -p /home/username/Downloads/
-v           : Verbose mode; also --debug
-f           : Force rewrite existing subtitles files; also --force
-u           : Generate the name using the path folder pieces; 
               also --use_pieces
-d deep      : Integer. Deep search. Default is 0 (means get first match), 
               1 (or more) is the quantity of pages to iterate (maximum 
               allowed value is 1); also --deep=deep
-m min_match : Float. Minimum match (%) to take into consideration. 
               Default is 0 (means any); also --min_match
-n           : Allow series detection in number format only (ie. Flash 101);
               also --number_format
-h           : Display help; also --help
```

## Requirements
```
Python 2.7
rarfile-2.6
rarosx-4.2.0 (on OSX) or similar
```

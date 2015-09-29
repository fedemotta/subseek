#!/usr/bin/env python
import urllib2
import os
import string
import chardet
import math
from datetime import datetime

import rarfile
import zipfile
from HTMLParser import HTMLParser

from constants import SUBTITLE_EXTENSION
from constants import SUBTITLE_LANGUAGE_FILTERS, SUBTITLE_LANGUAGE
from constants import SEASON_IN_VIDEO
from constants import EPISODE_IN_VIDEO
from constants import SEASON_IN_VIDEO_WITH_ZERO
from constants import EPISODE_IN_VIDEO_WITH_ZERO
from constants import SEASON_IN_SUB
from constants import EPISODE_IN_SUB
from constants import SEASON_IN_SUB_WITH_ZERO
from constants import EPISODE_IN_SUB_WITH_ZERO
from constants import START_YEAR
from constants import RELEASE_GROUPS, RESOLUTIONS, CODECS, RELEASE_TYPES


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)

    def get_data(self):
        return ' '.join(self.fed)


class Subseek():

    def get_files(self, path, extension):
        """
        Get all video files from a path
        """
        fileList = []
        rootdir = path
        # root, sub-folders and files
        for root, _, files in os.walk(rootdir):
            for one_file in files:
                if self.match_extension(one_file, '.' + extension) == True:
                    fileList.append(os.path.join(root, one_file))
        return fileList
    
    def detect_encoding(self, text):
        """
        Detect encoding of a given string
        """
        return  chardet.detect(text)['encoding']
    
    def remove_punctuation(self,text):
        """
        Remove duplicate spaces and non alphanumeric chars
        """
        # Replacing double spaces and other chars with single space
        text = text.translate(string.maketrans(string.punctuation, 
                            ' '*len(string.punctuation)))
        return  " ".join(text.split())
   
    def clean_text(self, text, filter_special_words=False, encoding='utf-8'):
        """
        Remove everything except alphanumeric, spaces and words from list
        """
        if encoding == None:
            encoding = 'utf-8'
        # decode with the provided encoding and always encode as utf-8
        text = text.decode(encoding,'ignore').lower().encode('utf-8','ignore')
        text = self.remove_punctuation(text)
        
        if filter_special_words:
            for word in (RELEASE_GROUPS + RESOLUTIONS + CODECS + RELEASE_TYPES):
                text = (' '+text+' ').replace(' '+ self.remove_punctuation(word.lower())+ ' ',' ')
            text = self.remove_punctuation(text)
            
        return text

    def name_and_filename(self, name, filename):
        """
        Remove duplicates words between name and filename
        """
        path_name_pieces = name.split()
        file_name_pieces = filename.split()
        for file_name_word in file_name_pieces:
            if file_name_word not in path_name_pieces:
                path_name_pieces.append(file_name_word)
        return ' '.join(path_name_pieces)

    def clean_name(self, name, filename, filter_special_words=False):
        """
        Clean name avoiding duplicates
        """
        name = self.clean_text(name, filter_special_words)
        filename = self.clean_text(filename, filter_special_words)
        return self.name_and_filename(name, filename)

    def get_filtered_words(self, text):
        """
        Get the filtered words from text
        """
        founds = self.get_release_groups(text)+self.get_resolutions(
                 text)+self.get_codecs(text)+ self.get_release_types(text)
        
        return founds

    def set_filtered_words(self, text, words):
        """
        Set filtered words to text
        """
        words_text = ' '.join(words)
        return text + ' ' + words_text

    def real_name(self, filename, path, rootpath=False, use_pieces=0, 
                                                            number_format=0):
        """
        Get search string and season-episode string from filename
        """
        # use pieces or not
        if use_pieces == 0:
            filtered_words = self.get_filtered_words(filename)
            name = self.clean_text(filename, True)
            name_no_filter = self.clean_text(filename, False)
        else:
            # get path pieces
            components = path.split(os.sep)
            # get root last folder
            if rootpath == False:
                rootpath = str(components[1])
            else:
                rootpath = str(rootpath.split(os.sep)[-2])

            name = ''

            # fix filename without full movie name
            for path_piece in reversed(list(components)):
                if rootpath == str(path_piece):
                    # @TODO: Add to path avoiding folders like "Downloads",
                    # Example:
                    # if rootpath != 'Downloads':
                    #     name = str(path_piece) + ' ' + name
                    break
                else:
                    name = str(path_piece) + ' ' + name

            filtered_words = self.get_filtered_words(self.name_and_filename(
                                                                        name,
                                                                      filename
                                                                       ))
            # clean avoiding duplicates
            name = self.clean_text(self.clean_name(name, filename, True), True)
            name_no_filter = self.clean_text(self.clean_name(name, filename,
                                                             False), False)

        seasonepisode = self.season_episode(name, number_format)
        
        # return search, season episode and search match
        if seasonepisode == False:
            return (self.fix_search(name), False,
                    self.fix_search(name_no_filter))
        else:
            return  (self.search_season_episode_name(name, seasonepisode),
                     seasonepisode,
                     # append filtered words to season episode name
                     self.set_filtered_words(self.search_season_episode_name(
                                             name, seasonepisode),
                                      filtered_words))

    def match_extension(self, filename, extension):
        """
        Check if it is a sub extension
        """
        if filename[len(filename) - len(extension):] == extension:
            return True
        else:
            return False

    def get_search_url(self, url, search, site=False):
        """
        Search url replacing search and site
        """
        if site == False:
            site = ''
        url = url.replace('{{SITE}}', "site:" + urllib2.quote(site))
        url = url.replace('{{SEARCH}}', urllib2.quote(search))
        return url

    def get_links(self, subtitle_search_engine, search, deep=0, site=False):
        """
        Get links from html
        """
        url = self.get_search_url(subtitle_search_engine['url'],
                                  search, site)
        data = subtitle_search_engine['data']

        html_links = self.get_html_links(url, data);
        
        # With deep=0 returns first match
        if deep==0 and html_links != False and len(html_links)>0:
            return [html_links[0]]
        else:
            # Avoid duplicates
            if html_links != False:
                html_links = [dict(t) for t in set([tuple(d.items()) for d in html_links])]

            return html_links

    def get_subtitles_links(self, link, subtitle_provider):
        """
        Get sub links from a subtitle provider
        """
        url = link
        data = subtitle_provider['data']
        force_download = subtitle_provider['force_download']
        html_links = self.get_html_links(url, data, False, True, force_download)
        
        return html_links

    def write_sub_file(self, real_file, filename):
        """
        Write subtitle file
        """
        d = open(filename[:-4] + '.' + SUBTITLE_EXTENSION, 'w')
        d.write(real_file)
        d.close()

    def order_file_list(self, search, info_list):
        """
        Order file list by order match
        """
        sub_list = []
        for file_from_list in info_list:
            sub_list.append({
                     "text": file_from_list.filename.lower(),
                     "description": "",
                     "real_file": file_from_list
                     })
        return self.order_match(search, sub_list, False)

    def decompress_file(self, filename):
        """
        Try to decompress a file
        """
        uncompressed_file = None
        try:
            uncompressed_file = rarfile.RarFile(filename)
            typefile = 'rar'
        except rarfile.NotRarFile:
            try:
                uncompressed_file = zipfile.ZipFile(filename)
                typefile = 'zip'
            except zipfile.BadZipfile:
                typefile = 'other'
        return uncompressed_file, typefile

    def other_language_sub(self, filename):
        """
        Check if this is another language sub
        """
        for lang, text in SUBTITLE_LANGUAGE_FILTERS.iteritems():
            if SUBTITLE_LANGUAGE != lang and not filename.find(text) == -1:
                return True
        return False

    def get_sub_file_from_file(self, filename, search, force):
        """
        Find the best subtitle file from a compressed file
        """
        uncompressed_file, typefile = self.decompress_file(filename)

        if not typefile == 'other':

            # order list of files to get the best match
            files = self.order_file_list(search, uncompressed_file.infolist())
            # flag for good file
            good = False

            for best_file in files:
                # check valid extension and already existent file
                if not good and self.match_extension(best_file["text"],
                    '.' + SUBTITLE_EXTENSION) == True and (not os.path.isfile(
                    filename[:-4] + '.' + SUBTITLE_EXTENSION) or force == 1
                    ) and not self.other_language_sub(best_file["text"]):
                        try:
                            self.write_sub_file(uncompressed_file.read(
                                                best_file["real_file"]),
                                                filename)
                            # keep only the subtitle file
                            os.remove(filename)
                            # break at first good subtitle
                            return typefile

                        except:
                            # keep iterating until a good file is found
                            good = False

        # remove bad file
        os.remove(filename)
        return False

    def download(self, url, dest):
        """
        Download file
        """
        try:
            s = urllib2.urlopen(url)
            content = s.read()
            s.close()
            d = open(dest, 'wb')
            d.write(content)
            d.close()
            return True
        except:
            return False
    
    def all_years(self):
        """
        Generates a year list
        """
        years = []
        year = START_YEAR
        while year <= datetime.now().year:
            years += [str(year)]
            year += 1
        
        return years
  
    def is_found(self, clean_text, search):
        """
        Find a search match a text
        """
        clean_search = ' '+self.clean_text(search)+' '
        if (' '+clean_text+' ').find(clean_search) != -1:
            return True
        else:
            return False
    
    def get_founds(self,text, list):
        """
        Returns a list of found
        """
        clean_text = self.clean_text(text)
        founds = []
        for search in list:
            if (self.is_found(clean_text, search)):
                founds += [self.clean_text(search)]
                
        return founds
    
    def get_years(self, text):
        """
        Find if the text has a year
        """
        return self.get_founds(text, self.all_years())
  
    def get_release_groups(self, text):
        """
        Find if the text has a release group
        """
        return self.get_founds(text, RELEASE_GROUPS)

    def get_resolutions(self, text):
        """
        Find if the text has a resolution
        """
        return self.get_founds(text, RESOLUTIONS)
    
    def get_codecs(self, text):
        """
        Find if the text has a codec
        """
        return self.get_founds(text, CODECS)
    
    def get_release_types(self, text):
        """
        Find if the text has a release type
        """
        return self.get_founds(text, RELEASE_TYPES)


    def get_season_episode_text(self, season=1,
                                episode=1,
                                season_search='s',
                                episode_search='e',
                                season_search_with_zero=True,
                                episode_search_with_zero=True,
                                ):
        """
        Generate the string for searching in the file name
        """
        if season_search == False:
            season_episode = ''
        else:
            season_episode = season_search
            if season_search_with_zero == True and season < 10:
                season_episode += '0'
            season_episode += str(season)

        if episode_search == False:
            return season_episode
        else:
            season_episode += episode_search
            if episode_search_with_zero == True and episode < 10:
                season_episode += '0'
            season_episode += str(episode)
            return season_episode
    
    def allow_season_episode_format(self, season_search, episode_search, 
                                                                number_format):
        """
        Allow or not some season episode format
        """
        if season_search in [False, '', ' '] and episode_search in [False, 
                                            '', ' '] and number_format == 0:
            return False
        return True
                                                
    def fix_season_episode_formatter(self, filename, season_search, 
                                    episode_search, number_format=0):
        """
        Avoid year, resolution and x264 errors
        """
        # get special words found to use later
        if season_search in [False, '', ' '] and ((episode_search in [False, 
            '', ' '] and number_format == 1) or (episode_search == 'x')):
            
            special_words_founds = self.get_years(filename
                    ) + self.get_release_groups(filename
                    ) + self.get_resolutions(filename
                    ) + self.get_codecs(filename
                    ) + self.get_release_types(filename)
            
        # remove year and any number word from the filename with 101 format
        if season_search in [False, '', ' '] and episode_search in [False, 
                                            '', ' '] and number_format == 1:
            for found in special_words_founds:
                if found.isdigit():
                    filename = (' '+filename+' ').replace(' '+found+' ', ' ')
            
            #remove numbers in search name
                
        # remove xNUMBER special word from the filename if x101 format
        if season_search in [False, '', ' '] and episode_search == 'x':
            for found in special_words_founds:
                if found[0]=='x' and found[:0].isdigit():
                    filename = (' '+filename+' ').replace(' '+found+' ', ' ')
        
        return " ".join(filename.split())
    
    def get_season_episode_formatter(self, filename, number_format=0,
                                    season_search='s',
                                    episode_search='e',
                                    season_search_with_zero=True,
                                    episode_search_with_zero=True,
                                    season_result='s',
                                    episode_result='e',
                                    season_result_with_zero=True,
                                    episode_result_with_zero=True,
                                    season_start=1,
                                    episode_start=1,
                                    season_end=99,
                                    episode_end=99
                                    ):
        """
        Format for season and episode in file name
        """
        # season and episode initial values
        season = season_start
        episode = episode_start
        
        if self.allow_season_episode_format(season_search, episode_search, 
                                                    number_format) == False:
            return False
        
        # remove special words which breaks the given formatter
        filename = self.fix_season_episode_formatter(filename, season_search, 
                                                  episode_search, number_format)
        
        while filename.find(self.get_season_episode_text(season,
                                             episode,
                                             season_search,
                                             episode_search,
                                             season_search_with_zero,
                                             episode_search_with_zero)) == -1:
            if (episode > episode_end):
                episode = 1
                season += 1
                if (season > season_end):
                    # not found
                    return False
            else:
                episode += 1
        return {'found': self.get_season_episode_text(season,
                                                    episode,
                                                    season_search,
                                                    episode_search,
                                                    season_search_with_zero,
                                                    episode_search_with_zero),
                'common': self.get_season_episode_text(season,
                                                    episode,
                                                    season_result,
                                                    episode_result,
                                                    season_result_with_zero,
                                                    episode_result_with_zero)
                }

    def season_episode(self, filename, number_format):
        """
        Search for season episode in name
        """
        seasonepisode = self.get_season_episode_formatter(filename, 
                                                          number_format)
        # search with many different formats
        # @TODO: Find a better way to do this loop
        for season_search in SEASON_IN_VIDEO:
            for episode_search in EPISODE_IN_VIDEO:
                for season_search_with_zero in SEASON_IN_VIDEO_WITH_ZERO:
                    for episode_search_with_zero in EPISODE_IN_VIDEO_WITH_ZERO:
                        for season_result in SEASON_IN_SUB:
                            for episode_result in EPISODE_IN_SUB:
                                for season_result_with_zero in SEASON_IN_SUB_WITH_ZERO:
                                    for episode_result_with_zero in EPISODE_IN_SUB_WITH_ZERO:
                                        seasonepisode = self.get_season_episode_formatter(filename,
                                                      number_format,
                                                      season_search,
                                                      episode_search,
                                                      season_search_with_zero,
                                                      episode_search_with_zero,
                                                      season_result,
                                                      episode_result,
                                                      season_result_with_zero,
                                                      episode_result_with_zero
                                                      )
                                        if not seasonepisode == False:
                                                return seasonepisode
        return seasonepisode

    def fix_search(self, filename, season=False):
        """
        Fixing filename to match some special cases
        """
        # @TODO: Use dictionaries to remove Spartacus, Zero Hour, shield
        # hard coded values
        if filename == 'spartacus' and season == 's01':
            return 'spartacus: blood and sand'
        elif filename == 'spartacus' and season == 's02':
            return 'spartacus: vengeance'
        elif filename == 'spartacus' and season == 's03':
            return 'spartacus: war of the damned'
        elif filename.find('zero hour') > -1:
            return 'zero hour'
        elif filename.find('marvels agents of s h i e l d') > -1:
            return 'agents of s.h.i.e.l.d'
        # @TODO: Use dictionaries to remove Justice League hard coded values
        # for justice league complete series, this is a mess,
        # but was the main reason of the creation of this script, because
        # the folders and filenames are all mashup
        elif filename[0:3] == 'jl ':

            start = 4
            if filename[4:5].isdigit() == True:
                start = 5
            if filename[5:6].isdigit() == True:
                start = 6
            if filename[6:7].isdigit() == True:
                start = 7
            if filename[7:8].isdigit() == True:
                start = 8
            if filename[8:9].isdigit() == True:
                start = 9

            if filename[-2:len(filename) - 1] == 'u':
                return ('justice league unlimited ' +
                         filename[start:len(filename) - 2]).replace('  ', ' ')
            else:
                return ('justice league ' +
                         filename[start:len(filename)]).replace('  ', ' ')
        else:
            return filename

    def search_season_episode_name(self, filename, seasonepisode):
        """
        Search name using season episode name
        """
        return self.fix_search(filename[:filename.find(
                                             seasonepisode['found']) - 1],
                                             seasonepisode['found'][:3]
                                             ) + ' ' + seasonepisode['common']

    def clean_html(self, html):
        """
        Remove html tags
        """
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def get_html_links(self, url, data, filter_site_url=False,
                       clean_html=True,force_download=False):
        """
        Search links using a dictionary data
        """
        results = []
        # google returns 403 without user agent
        headers = {'User-agent': 'Mozilla/11.0'}
        req = urllib2.Request(url, None, headers)
        try:
            site = urllib2.urlopen(req)
        except:
            return False

        html_data = ' '.join(site.read().split())
        site.close()
        start = html_data.find(data['start_all'])
        end = html_data.find(data['end_all'])

        if html_data[start:end] == '':
            # error, no links to find
            results = []
        else:
            html_data = html_data[start:end]
            start = 0
            end = 0
            while start > -1 and end > -1:
                # get result block
                start = html_data.find(data['start_one'])
                html_data = html_data[start + len(data['start_one']):]
                end = html_data.find(data['end_one'])
                if start > -1 and end > -1:
                    # get text
                    starttext = html_data.find(data['start_text'])
                    datatext = html_data[starttext + len(data['start_text']):]
                    endtext = datatext.find(data['end_text'])
                    if starttext > -1 and endtext > -1:
                        text = datatext[0:endtext]
                    else:
                        text = ''

                    # get description
                    startdescription = html_data.find(
                                                    data['start_description']
                                                    )
                    datadescription = html_data[startdescription + len(
                                                    data['start_description']
                                                    ):]
                    enddescription = datadescription.find(
                                                    data['end_description']
                                                    )
                    if startdescription > -1 and enddescription > -1:
                        description = datadescription[0:enddescription]
                    else:
                        description = ''

                    # get only results of the provided site
                    if filter_site_url == False:
                        startlink = html_data.find(data['start_link'])
                    else:
                        startlink = html_data.find(
                                    data['start_link'] + str(filter_site_url)
                                    )

                    datalink = html_data[startlink + len(data['start_link']):]
                    endlink = datalink.find(data['end_link'])

                    if start > -1 and end > -1:
                        if force_download == False:
                            link = urllib2.unquote(datalink[0:endlink])
                        else:
                            # force downlad url is the first result of another link
                            link_force = self.get_html_links(datalink[0:endlink], force_download)
                            if link_force==False:
                                link = ''
                            else:
                                link = urllib2.unquote(link_force[0]['link'])
                        if link.find('http') == 0:
                            if clean_html:
                                description = self.clean_html(description)
                            results.append({
                                    'link': link,
                                    'text': text,
                                    'description': description
                                    })

                # move to next block
                html_data = html_data[end:len(html_data)]
        return results

    def split_every_n(self, n, text):
        """
        Split the text in n pieces
        """
        wordssplit = []
        auxwords = []
        words = text.split()
        count = 0
        for word in words:
            if count == n - 1:
                auxwords.append(word)
                wordssplit.append(' '.join(auxwords))
                # reset
                auxwords = []
                count = 0
            else:
                auxwords.append(word)
                count = count + 1
        return wordssplit

    def text_weight(self, text, match=False, n=False):
        """
        Weight rating a string match. Uses (2*n)**(weightaux)
        where n is the string length and weightaux is calculated with the
        length and position of the word
        """
        text = text.lower()
        if not match is False:
            match = match.lower()
        weight = 0
        if not n:
            n = len(text.split())
        else:
            # use only the first n words
            text = ' '.join(text.split(' ', n))
            if match is not False:
                match = ' '.join(match.split(' ', n))
        while n > 0:
            words = self.split_every_n(n, text)
            pos = len(words)
            weightaux = 0
            for word in words:
                if match == False:
                    weightaux = weightaux + len(word) * pos
                else:
                    if match.find(' ' + word + ' ') > -1:
                        weightaux = weightaux + len(word) * pos
                pos = pos - 1
            weight = weight + (2 * n) ** (weightaux)
            n = n - 1
        # Use log 10 for readability     
        return math.log10(weight)

    def order_match(self, search, results, clean=True):
        """
        Return the list of results ordered by weight
        """
        return sorted(results, key=lambda t: (self.text_weight(search,
                            (self.clean_text(t['text'], False, 
                            self.detect_encoding(t['text'])
                            ) if clean else t['text'])  + " " +
                            (self.clean_text(t['description'], False, 
                            self.detect_encoding(t['description'])
                            ) if clean else t['description']))), 
                            reverse=True)

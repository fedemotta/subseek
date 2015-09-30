from constants import (SUBTITLE_SEARCH_ENGINES, SUBTITLE_PROVIDERS,
                              SEARCH_ENGINES)
from models import Subseek


def get_files(path, extension):
    """
    Use get_files method
    """
    return Subseek().get_files(path, extension)


def real_name(filename, path, rootpath, use_pieces, number_format):
    """
    Use real_name method
    """
    return Subseek().real_name(filename, path, rootpath, use_pieces, 
                                number_format)


def download_subtitle(search, results, filename, min_match=0,
                      force=0, debug=0):
    """
    Download for real the best subtitle
    """
    s = Subseek()
    subtitleurl = False
    for result in s.order_match(search, results):
        match_text = s.clean_text(result['text'],False, 
                    s.detect_encoding(result['text'])
                    ) + " " + s.clean_text(result['description'],False, 
                    s.detect_encoding(result['description']))
        subtitleurl = result['link']
        rating_weight = s.text_weight(search, match_text)
        max_weight = s.text_weight(search)
        rating_match = rating_weight/max_weight*100
        if debug == 1:
            print "Subtitle File URL: " + subtitleurl
            print "   Text To Search: " + search
            print "    Text To Match: " + match_text
            print "   Text Match (%): " + str(round(rating_match,2)) + "%"
        # check minimal match to use
        if rating_match >= min_match:
            downloaded = s.download(subtitleurl, filename + '.tmp')
            if downloaded == False:
                if debug == 1:
                    print "Error: connection or file creation failed"
                subtitleurl = False
            else:
                if debug == 1:
                    print "File downloaded"
                # unrar, unzip or get srt file
                typefile = s.get_sub_file_from_file(filename + '.tmp',
                                                    search, force)
                if typefile == False:
                    if debug == 1:
                        print "Subtitle file not found"
                    subtitleurl = False
                else:
                    if debug == 1:
                        print "Subtitle file found in " + typefile
                    subtitleurl = True
                    break
        else:
            if debug == 1:
                print "Error: match less than " + str(round(min_match,2))+ "%"
            subtitleurl = False
            break

    return subtitleurl


def subtitle_search_engines_links(search, deep=0, debug=0, links=[]):
    """
    Search the subtitle using subtitle search engines and
    get all the links from all
    """
    s = Subseek()
    for subtitle_search_engine in SUBTITLE_SEARCH_ENGINES:
        if debug == 1:
            print "Searching '%s' in '%s'" % (search,
                                            subtitle_search_engine['name'])
        links_aux = s.get_links(subtitle_search_engine, search, deep)
        if not links_aux or len(links_aux) == 0:
            if debug == 1:
                print "No match found in '%s'" % subtitle_search_engine['name']
        else:
            if debug == 1:
                print "%s matches found in '%s'" % (len(links_aux),
                                               subtitle_search_engine['name'])

            links = links_aux + links

    return links


def external_search_engines_links(search, deep=0, debug=0, links=[]):
    """
    Search the subtitle using external search engines and
    get all the links from all
    """
    s = Subseek()
    for search_engine in SEARCH_ENGINES:
        for subtitle_search_engine in SUBTITLE_SEARCH_ENGINES:
            if debug == 1:
                print "Searching '%s' in '%s'" % (search,
                                                  search_engine['name'])
            links_aux = s.get_links(search_engine, search, deep,
                                    subtitle_search_engine["name"])
            if not links_aux or len(links_aux) == 0:
                if debug == 1:
                    print "No match found in '%s'" % search_engine['name']
            else:
                if debug == 1:
                    print "%s matches found in '%s'" % (len(links_aux),
                                                   search_engine['name'])
                links = links_aux + links

    return links


def download_best_subtitle(links, full_search, path_file_name,
                           min_match=0, force=0, debug=0):
    """
    Download the best subtitle of a given list of links
    """
    s = Subseek()
    if not links or len(links) == 0:
        return False
    else:
        results = []
        for link in links:
            if debug == 1:
                print "Searching in " + link['link']
            for provider in SUBTITLE_PROVIDERS:
                results_aux = s.get_subtitles_links(link['link'],
                                                       provider)
                if results_aux is False or len(results_aux) == 0:
                    if  debug == 1:
                        print "No subtitles with '%s'" % provider['name']
                else:
                    if  debug == 1:
                        print "%s subtitles with '%s'" % (len(results_aux),
                                                   provider['name'])
                    results = results + results_aux
        # download the best subtitle of the entire list
        return download_subtitle(full_search,
                                 results,
                                 path_file_name,
                                 min_match,
                                 force,
                                 debug)


def best_subtitle_url(search, full_search, path_file_name,
                      min_match=0, force=0, deep=0, debug=0):
    """
    Get the best subtitle url
    """
    # first search in subtitle search engines
    links = subtitle_search_engines_links(search, deep, debug)
    subtitle_url = download_best_subtitle(links,
                                          full_search,
                                          path_file_name,
                                          min_match, force, debug)
    # if not found use the external search engines
    if not subtitle_url:
        links = external_search_engines_links(search, deep, debug)
        subtitle_url = download_best_subtitle(links,
                                              full_search,
                                              path_file_name,
                                              min_match, force, debug)

    return subtitle_url

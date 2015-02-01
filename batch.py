#!/usr/bin/env python
import os
from console.options import options, start
from core import (VIDEO_EXTENSIONS, SUBTITLE_EXTENSION, real_name,
                     best_subtitle_url, get_files)


def main(argv):
    # These are features under development:
    # 1) @TODO: Generate the name using the path folder pieces. This is
    # working but we need to find a way to detect automatically when using
    # pieces or not.
    # 2) @TODO: Avoid subtitle match with less than a minimal weight. This is
    # working but needs more testing, and the value should be a smaller number
    # like 1, 2, 5, etc.
    # 3) @TODO: Words to add to the special words list.
    # 4) @TODO: Deep of the search (-d). Default is 0 and get first match. 1 or
    # more is the quantity of pages to iterate on each search.
    min_weigth = 0

    # get options from parameters
    rootpath, debug, force, use_pieces = options(argv)
    for extension in VIDEO_EXTENSIONS:
        for infile in get_files(rootpath, extension):
            # remove path and extension
            filename = os.path.basename(infile)[:-len(extension) - 1]
            path = os.path.dirname(infile) + os.sep
            if debug == 1:
                print """
-------------------------------------------------------------------------------
                      """
                print 'Starting process for "' + path + filename + '"'

            # do not search if already have subtitles and not force mode
            # @TODO: Allow different subtitle types
            if force == 0 and os.path.isfile(path + filename + '.' +
                                             SUBTITLE_EXTENSION):
                if debug == 1:
                    print 'Subtitle already exists'
            else:
                # find season and episode in file name or path (use_pieces),
                # search and full search
                search, season_episode, full_search = real_name(filename,
                                                                path,
                                                                rootpath,
                                                                use_pieces)
                if (season_episode == False):
                    if debug == 1:
                        print 'Not valid series name'
                else:
                    if debug == 1:
                        print 'Valid series name'

                subtitle_url = best_subtitle_url(search,
                                                 full_search,
                                                 path + filename,
                                                 min_weigth,
                                                 force,
                                                 debug)
                if subtitle_url is False:
                    if debug == 1:
                        print "Best subtitle not found"

            if debug == 1:
                print 'Ending process for "' + path + filename + '"'
                print """
-------------------------------------------------------------------------------
                      """

# start abd get params
if __name__ == "__main__":
    start(main)
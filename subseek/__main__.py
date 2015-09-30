#!/usr/bin/env python
import os
from options import options, start
from constants import (VIDEO_EXTENSIONS, SUBTITLE_EXTENSION)
from utils import (real_name, best_subtitle_url, get_files)


def main(argv):
    # These are features under development:
    # 1) @TODO: Generate the name using the path folder pieces. This is
    # working but we need to find a way to detect automatically when using
    # pieces or not.
    # 3) @TODO: Words to add to the special words list.
    # 4) @TODO: Add deep search higher than 1 using pagination links
    
    # get options from parameters
    rootpath,debug,force,use_pieces,deep,min_match,number_format = options(argv)
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

            # do not search if already have subtitles and is not in force mode
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
                                                                use_pieces,
                                                                number_format)
                if search == 'sample':
                    if debug == 1:
                        print 'Not searching subtitle for sample file'
                else:
                    if (season_episode == False):
                        if debug == 1:
                            print 'Not valid series name'
                    else:
                        if debug == 1:
                            print 'Valid series name'

                    subtitle_url = best_subtitle_url(search,
                                                     full_search,
                                                     path + filename,
                                                     min_match,
                                                     force,
                                                     deep,
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

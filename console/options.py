import sys
import getopt


def usage():
    return  """
    Usage        : python console.py -p (path) [option]
    Options and arguments:
    -p path      : Required. As string. Root path to start the process; 
                   also --path=path. 
                   Example: python console.py -p /home/username/Downloads/
    -v           : Verbose mode; also --debug
    -f           : Force rewrite existing subtitles files; also --force
    -u           : Generate the name using the path folder pieces; 
                   also --use_pieces
    -d deep      : Deep search. As integer. 0 means get first match, 1 (or more) 
                   is the quantity of pages to iterate (maximum allowed value is
                   1); also --deep=deep
    -m min_match : Minimum match (%) to take into consideration. As float. 
                   Default is 0 (means any); also --min_match
    -h           : Display help; also --help
    """


def options(argv):
    # default values
    rootpath = False
    debug = 0
    force = 0
    use_pieces = 0
    deep = 0
    min_match = 0
    try:
        opts, _ = getopt.getopt(argv, "hfup:d:m:v", ["help", "force", 
                        "use_pieces", "path=", "deep=", "min_match=", "debug"])
    except getopt.GetoptError:
        print usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage()
            sys.exit()
        elif opt in ("-v","--debug"):
            debug = 1
        elif opt in ("-p", "--path"):
            rootpath = arg
        elif opt in ("-f", "--force"):
            force = 1
        elif opt in ("-u", "--use_pieces"):
            use_pieces = 1
        elif opt in ("-d", "--deep"):
            deep = int(arg)
        elif opt in ("-m", "--min_match"):
            min_match = float(arg)
        
    if rootpath == False:
            print usage()
            sys.exit(2)
        
    return [rootpath, debug, force, use_pieces, deep, min_match]


def start(func):
    func(sys.argv[1:])

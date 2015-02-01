import sys
import getopt


def usage():
    return  """
    Usage: python console.py -p (path) [option]
    Options and arguments:
    -p path : Required. Root path to start the process; also --path=path.
    Example: python console.py -p /home/username/Downloads/
    -f      : Force rewrite existing files; also --force
    -v      : Verbose mode
    -u      : Generate the name using the path folder pieces
    -h      : Help; also --help
    """


def options(argv):
    # default values
    rootpath = False
    debug = 0
    force = 0
    use_pieces = 0
    try:
        opts, _ = getopt.getopt(argv, "hfup:v", ["help", "force", "use_pieces",
                                                  "path="])
    except getopt.GetoptError:
        print usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage()
            sys.exit()
        elif opt == '-v':
            debug = 1
        elif opt in ("-p", "--path"):
            rootpath = arg
        elif opt in ("-f", "--force"):
            force = 1
        elif opt in ("-u", "--use_pieces"):
            use_pieces = 1
    if rootpath == False:
            print usage()
            sys.exit(2)
    return [rootpath, debug, force, use_pieces]


def start(func):
    func(sys.argv[1:])

# Search in video file (used to generate a valid series name)
# All combined season episodes tags here. '' and "False" should be last or
# could be overrides
SEASON_IN_VIDEO = ['s', '', False]
EPISODE_IN_VIDEO = ['e', ' e', 'x', 'ep', 'episode ', ' ', '']
SEASON_IN_VIDEO_WITH_ZERO = [False, True]
EPISODE_IN_VIDEO_WITH_ZERO = [True, False]
# Search in subtitle (the online search)
SEASON_IN_SUB = ['s']
EPISODE_IN_SUB = ['e']
SEASON_IN_SUB_WITH_ZERO = [True]
EPISODE_IN_SUB_WITH_ZERO = [True]

# File extensions
VIDEO_EXTENSIONS = ['avi', 'mp4', 'mkv', 'mpg', 'mpeg', 'flv']
SUBTITLE_EXTENSION = 'srt'

# Special words to filter in lower case, first words overrides last words,
# because when there is a found the word is removed from the text,
# @TODO: Order this list by word length before using it.
SPECIAL_WORDS = [
                'bdrip',
                'cam',
                'dvdrip',
                'dvdscr',
                'hdrip',
                'r6',
                'r5',
                'rc',
                'scr',
                'telecine',
                'telesync',
                'workprint',
                'xvid',
                'reencx264-bob',
                'x264',
                'hdrip',
                '720p',
                '1080p',
                '480p',
                'ac3',
                'web-dl',
                'dvd-rip',
                'bluray',
                'www.torrenting.com',
                'brrip',
                'www.usabit.com',
                'yify',
                'hdtv',
                'asap',
                'saints',
                'vlis',
                'evolve',
                'bito',
                'ts',
                's4a',
                'juggs',
                ]

# starting year
START_YEAR = 1900

# resolutions
RESOLUTIONS = ['480', '720', '1080']

# Subtitles languages
SUBTITLE_LANGUAGE = 'es'

SUBTITLE_LANGUAGE_FILTERS = {'en': '[english',
                             'es': '[espanol',
                             'it': '[italiano'}

# Dictionaries to search
SUBTITLE_SEARCH_ENGINES = [
    {'name': 'www.subdivx.com',
     'url': 'http://www.subdivx.com/index.php?accion=5&masdesc=&buscar={{SEARCH}}&oxdown=1',
     'data':{
             'start_all': '<div id="menu_detalle_buscador">',
             'end_all': '<div id="pie">',
             'start_one': '<div id="menu_titulo_buscador">',
             'end_one': '</div></div>',
             'start_link': '<a class="titulo_menu_izq" href="',
             'end_link': '">',
             'start_text': '">',
             'end_text': '</a>',
             'start_description': '<div id="buscador_detalle_sub">',
             'end_description': '</div><div id="buscador_detalle_sub_datos">'
         }
        }]

SEARCH_ENGINES = [
     {'name': 'http://www.google.com',
     'url': 'http://www.google.com/search?q={{SITE}}%20{{SEARCH}}&oq={{SITE}}%20{{SEARCH}}',
     'data':{
          'start_all': '<div id="ires">',
          'end_all': '<div id="foot">',
          'start_one':'<li class="g">',
          'end_one':'</li>',
          'start_link':'<a href="/url?q=',
          'end_link':'&amp;sa=U&amp;ei=',
          'start_text':'<a href="/url?q=',
          'end_text':'</a>',
          'start_description':'<span class="st">',
          'end_description':'</span>',
      }
     },
    {'name': 'http://www.duckduckgo.com',
     'url': 'http://duckduckgo.com/html/?q={{SITE}}%20{{SEARCH}}',
     'data':{
          'start_all': '<div id="links_wrapper">',
          'end_all': '<div class="results_links_more nav-link">',
          'start_one': '<div class="links_main links_deep">',
          'end_one': '</div> </div> </div>',
          'start_link': '<a rel="nofollow" class="large" href="',
          'end_link': '">',
          'start_text': '">',
          'end_text': '</a>',
          'start_description': '<div class="snippet">',
          'end_description': '</div>',
      }
    }]

SUBTITLE_PROVIDERS = [
    {'name': 'New subdivx.com subtitle page',
     'data':{
        'start_all': '<div id="menu_detalle_buscador">',
        'end_all': '<div id="pie">',
        'start_one': '<div id="menu_titulo_buscador">',
        'end_one': '</a><br><br></div>',
        'start_link': '</b></a> - <a class="detalle_link" href="',
        'end_link': '"><b>Bajar</b>',
        'start_text': '">',
        'end_text': '</div>',
        'start_description': '<div id="detalle_datos">',
        'end_description': '</div>'
        }
    },
    {'name': 'Old subdivx.com subtitle page',
      'data':{
            'start_all': '<div id="menu_detalle_buscador">',
            'end_all': '<div id="pie">',
            'start_one': '<div id="menu_titulo_buscador">',
            'end_one': '<div id="contenedor_der">',
            'start_link': '<center><h1><a class="link1" href="',
            'end_link': '">Bajar subt',
            'start_text': '<b>',
            'end_text': '</b>',
            'start_description': '<div id="detalle_datos">',
            'end_description': '</div>'
            }
     },
     {'name': 'Old subdivx.com index page',
      'data':{
        'start_all': '<div id="menu_detalle_buscador">',
        'end_all': '<div id="pie">',
        'start_one': '<div id="menu_titulo_buscador">',
        'end_one': '<img src="bajar_sub.gif" border="0"></a></div></div>',
        'start_link': '<a rel="nofollow" target="new" href="',
        'end_link': '"><img src="bajar_sub.gif" border="0"></a>',
        'start_text': '">',
        'end_text': '</a>',
        'start_description': '<div id="buscador_detalle_sub">',
        'end_description': '</div><div id="buscador_detalle_sub_datos">'
        }
     },
    ]

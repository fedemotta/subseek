# Search in video file (used to generate a valid series name)
# All combined season episodes tags here. '' and "False" should be last or
# could be overrides
SEASON_IN_VIDEO = ['s', '', False]
EPISODE_IN_VIDEO = ['e', ' e', 'x','#', 'ep', 'episode ', ' ', '']
SEASON_IN_VIDEO_WITH_ZERO = [False, True]
EPISODE_IN_VIDEO_WITH_ZERO = [True, False]
# Search in subtitle (the online search)
SEASON_IN_SUB = ['s']
EPISODE_IN_SUB = ['e']
SEASON_IN_SUB_WITH_ZERO = [True]
EPISODE_IN_SUB_WITH_ZERO = [True]

# Banned search
BANNED_SEARCH = ['sample',' ','']

# File extensions
VIDEO_EXTENSIONS = ['avi', 'mp4', 'mkv', 'mpg', 'mpeg', 'flv']
SUBTITLE_EXTENSION = 'srt'

# starting year
START_YEAR = 1900

# release groups
RELEASE_GROUPS = [
        'BOB',
        'AC3',
        'www.torrenting.com',
        'www.usabit.com',
        'www.pimp4003.net',
        'Pimp4003',
        'YIFY',
        'LOL',
        'ASAP',
        'SAINTS',
        'VLIS',
        'EVOLVE',
        'BITO',
        'S4A',
        'JUGGS',
        'ETRG.com',
        'RARBG.com',
        'ETRG',
        'RARBG',
        '2HD',
        'AAC',
        'mSD',
        'REWARD',
        'AMIABLE',
        'ENCODEKING',
        'KILLERS',
        'OZLEM',
        'EVO',
        'anoXmous'
    ]

# resolutions
RESOLUTIONS = [
        'SVCD',
        '480',
        '480i',
        '480p',
        '576',
        '576i',
        '576p',
        'DVD',
        '720', 
        '720p',
        '1080',
        '1080p',
        '1080i',
        '2160',
        '2160p',
        '4320',
        '4320p'
]

# codecs
CODECS = [
        'mp3',
        'mp4',
        'x265',
        'REENCx264',
        'x264',
        'DivX',
        'Xvid',
        'FFmpeg',
        '3ivx',
        'x262',
        'WMV',
        'VP6', 
        'VP6-E',
        'VP6-S',
        'VP7',
        'VP8',
        'VP9',
        'libtheora',
        '6CH'
]
            
# release types
RELEASE_TYPES = [
        'CAMRip',
        'CAM',
        'TS',
        'TELESYNC',
        'PDVD',
        'WP',
        'WORKPRINT',
        'TC',
        'TELECINE',
        'PPV',
        'PPVRip',
        'SCR',
        'SCREENER',
        'DVDSCR',
        'DVDSCREENER',
        'BDSCR',
        'DDC',
        'RC',
        'R5',
        'R5.LINE',
        'R5.AC3.5.1.HQ',
        'R0',
        'R1',
        'R2',
        'R3',
        'R4',
        'R6',
        'R7',
        'R8',
        'R9',
        'DVDRip',
        'DVDR', 
        'DVD-Full',
        'Full-Rip', 
        'ISO rip', 
        'lossless rip',
        'untouched rip', 
        'DVD-5',
        'DVD-9',
        'DSR',
        'DSRip',
        'DTHRip',
        'DVBRip',
        'HDTV',
        'PDTV',
        'TVRip',
        'HDTVRip',
        'HDRip',
        'VODRip',
        'VODR',
        'WEBDL',
        'WEB-DL',
        'WEB-Rip',
        'WEBRIP',
        'WEB-Cap',
        'WEBCAP',
        'BDRip',
        'BRRip',
        'Blu-Ray', 
        'BluRay', 
        'BLURAY',
        'BDR',
        'BD5',
        'BD9', 
        'BD25',
        'BD50',
]

# Subtitles languages
SUBTITLE_LANGUAGE = 'es'

SUBTITLE_LANGUAGE_FILTERS = {'en': '[english',
                             'es': '[espanol',
                             'it': '[italiano'}

# Dictionaries to search
SUBTITLE_SEARCH_ENGINES = [
    {'name': 'subdivx.com',
     'url': 'http://www.subdivx.com/index.php?accion=5&masdesc=&buscar={{SEARCH}}&oxdown=1',
     'data':{
             'start_all': '<div id="contenedor_izq"',
             'end_all': '<div id="contenedor_der"',
             'start_one': '<div id="menu_detalle_buscador"',
             'end_one': '<div id="buscador_detalle_sub_datos"',
             'start_link': '<a class="titulo_menu_izq2" href="',
             'end_link': '">',
             'start_text': '">',
             'end_text': '</a>',
             'start_description': '<div id="buscador_detalle_sub">',
             'end_description': '</div><div id="buscador_detalle_sub_datos">'
         }
        }]

SEARCH_ENGINES = [
    {
    'name': 'google.com',
    'url': 'http://www.google.com/search?q={{SITE}}%20{{SEARCH}}&oq={{SITE}}%20{{SEARCH}}',
    'data':{
        'start_all': '<div id="ires">',
        'end_all': '<div id="foot">',
        'start_one':'<li class="g">',
        'end_one':'</li>',
        'start_link':'<a href="/url?q=',
        'end_link':'&amp;sa=U&amp',
        'start_text':'<a href="/url?q=',
        'end_text':'</a>',
        'start_description':'<span class="st">',
        'end_description':'</span>',
        }
    },
    {
    'name': 'duckduckgo.com',
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
    }
]

SUBTITLE_PROVIDERS = [
    {
    'name': 'www.subdivx.com subtitle page',
    'data':{
        'start_all': '<div id="contenedor_interno"',
        'end_all': '<div id="pie">',
        'start_one': '<div id="contenedor_izq"',
        'end_one': '<div id="contenedor_der"',
        'start_link': '<a rel="nofollow" class="detalle_link" href="',
        'end_link': '"><b>Bajar</b></a>',
        'start_text': '<b>',
        'end_text': '</b>',
        'start_description': '<br><br><font size=4>',
        'end_description': '</font><br>'
        },
    'force_download':{
        'start_all': '<body',
        'end_all': '</body>',
        'start_one': 'Por favor utiliza el',
        'end_one': '</a>',
        'start_link': "<a href='",
        'end_link': "'><u>link directo",
        'start_text': 'Por favor utiliza el',
        'end_text': '</a>',
        'start_description': 'Por favor utiliza el',
        'end_description': '</a>'
        }
    },
    {
    'name': 'www.subdivx.com search page',
    'url': 'http://www.subdivx.com/index.php?accion=5&masdesc=&buscar={{SEARCH}}&oxdown=1',
    'data':{
        'start_all': '<div id="contenedor_izq"',
        'end_all': '<div id="contenedor_der"',
        'start_one': '<div id="menu_detalle_buscador"',
        'end_one': '<div id="buscador_detalle_sub_datos"',
        'start_link': '<a class="titulo_menu_izq2" href="',
        'end_link': '">',
        'start_text': '">',
        'end_text': '</a>',
        'start_description': '<div id="buscador_detalle_sub">',
        'end_description': '</div><div id="buscador_detalle_sub_datos">'
        },
    'force_download':False
    }
]

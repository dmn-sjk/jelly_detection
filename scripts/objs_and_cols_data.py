class_inds = {'snake': {'yellow': 14, 'even_lighter_red': 14,
                        'black': 13, 'orange': 13,
                        'green': 12, 'white': 12},
              'circle': {'light_red': 6,
                         'dark_red': 7,
                         'orange': 8,
                         'green': 9,
                         'yellow': 10,
                         'white': 11},
              'bear': {'light_red': 0,
                       'dark_red': 1,
                       'orange': 2,
                       'green': 3,
                       'yellow': 4,
                       'white': 5}}

hsv_lows = {'light_red': (0, 142, 93),
            'dark_red': (156, 154, 78),
            'orange': (10, 111, 87),
            'green': (25, 114, 33),
            'yellow': (22, 148, 61),
            'black': (0, 0, 0),
            'even_lighter_red': (177, 156, 146)}

hsv_highs = {'light_red': (6, 255, 255),
             'dark_red': (191, 255, 123),
             'orange': (18, 240, 255),
             'green': (76, 255, 147),
             'yellow': (29, 255, 255),
             'black': (255, 188, 57),
             'even_lighter_red': (182, 255, 251)}

col_name_list = list(hsv_lows.keys())
col_low_list = list(hsv_lows.values())
col_high_list = list(hsv_highs.values())

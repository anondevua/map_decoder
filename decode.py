
import argparse
import struct
import pynmea2
import logging

COMMON_DATA = "3I2h8I"

class FileEndedException(BaseException):
    pass

class WayListInfo:

    def __init__(self):
        self.name = ''
        self.some_info = []
        self.points = [] # lists of points

    def __repr__(self):
        return 'WayListInfo [{}]'.format(self.name) # + '\n{}'.format(self.main_data)
    
    def find_point(self, name):
        for p in self.points:
            if p.name == name:
                return p
        return None

class WLPoint:
    def __init__(self):
        self.some_flag = 0
        self.some_flag_two = 0
        self.some_flag_three = 0
        self.name = ''
        self.main_data = [] # 52 bytes

    def __repr__(self):
        return 'WLPoint "{}"\n{}'.format(self.name, self.main_data)

class PointInfo:
    name = ""
    user_name = []
    main_data = []

    def __repr__(self):
        return 'PointInfo "{}" [{}]'.format(self.name, self.user_name) + '\n{}'.format(self.main_data)

def values(f, fmt):
    size = struct.calcsize(fmt)
    data = f.read(size)
    if (len(data) != size):
        raise FileEndedException()
    return struct.unpack(fmt, data)

def value(f, fmt):
    return values(f, fmt)[0]

def decode_RF_PL(fs):
    results = []
    try:
        while True:
            new_point = PointInfo()
            name_length = value(fs, "<I")
            new_point.name = value(fs, "<{}s".format(name_length)).decode('utf-8')
            user_name_length = value(fs, "<I")
            new_point.user_name = value(fs, "<{}s".format(user_name_length)).decode('windows-1251')

            new_point.main_data = values(fs, "<{}".format(COMMON_DATA))
            results.append(new_point)
    except FileEndedException:
        logging.debug("file ended")

    return results

def decode_RF_WL(fs):
    result = []
    try:
        while True:
            wl = WayListInfo()
            hdr_data_length = value(fs, "<I")
            wl.name = value(fs, "<{}s".format(hdr_data_length)).decode('windows-1251')
            some_info_length = value(fs, "<I")
            wl.some_info = value(fs, "<{}s".format(some_info_length))
            points_count = value(fs, "<I")
            for pnum in range(points_count):
                np = WLPoint()
                name_length = value(fs, "<I")
                np.name = value(fs, "<{}s".format(name_length)).decode('windows-1251')
                np.some_flag_two = value(fs, '<I')
                np.main_data = values(fs, '<I{}'.format(COMMON_DATA))
                # pynmea2.parse()
                # np.some_flag_three = value(fs, '<I')
                wl.points.append(np)
            result.append(wl)

    except FileEndedException:
        logging.debug("file ended")
    return result

def scan_PL(file_path):
    logging.info('== scanning pointlist ==')
    results = []
    with open(file_path, 'rb') as f:
        results = decode_RF_PL(f)
    for r in results:
        logging.debug(r)
    return results

def scan_WL(file_path):
    logging.info('== scanning waylist ==')
    wl_result = None
    with open(args.w, 'rb') as f:
        wl_result = decode_RF_WL(f)

    for wl in wl_result:
        logging.debug(wl)
        for r in wl.points:
            logging.debug(r)
    return wl_result

if __name__ == '__main__':
    logging.basicConfig(
        filename='out.log',
        filemode='wt',
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(
        description='Russian warship idi nahui'
    )
    parser.add_argument('-w', metavar='waylist',
                        required=True, help='waylist file path')
    parser.add_argument('-p', metavar='pointlist',
                        required=True, help='pointlist file path')

    args = parser.parse_args()
    
    point_list = scan_PL(args.p)
    waylists = scan_WL(args.w)
    try:
        for p in point_list:
            for w in waylists:
                wp = w.find_point(p.name)
                if wp:
                    logging.info('Point found. WL:\n{}\nPL:\n{}'.format(wp, p))
                    raise RuntimeError()
    except RuntimeError as e:
        pass 

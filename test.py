import unittest
import logging
from decode import decode_RF_WL, decode_RF_PL

class TestStringMethods(unittest.TestCase):

    def test_mykolayiv_wl(self):
        arg = 'mykolaiv/routedatabase.waylist'
        result = []
        with open(arg, 'rb') as f:
            result = decode_RF_WL(f)
        logging.info(result.header)
        logging.info(result.some_info)
        for r in result.points:
            logging.info(r)

    # def test_mykolayiv_pl(self):
    #     arg = 'mykolaiv/waypointdatabase.pointlist'
    #     result = []
    #     with open(arg, 'rb') as f:
    #         result = decode_RF_PL(f)

    #     for r in result:
    #         # if r.name == "P0306-01":
    #         logging.info(r)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
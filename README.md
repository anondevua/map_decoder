# map_decoder

This tool allows to reproduce GPX waypoints from orcs navigators (14Ц8009) into map, including dates and names of points.

## Installation

Install dependencies

```bash
pip3 install -r requirements.txt
```

## Usage

- Turn on navigator with inserted card
- Select *Export to SD card* option in Settings
  This converts binary saved data into XML file (see [GPX format description](https://docs.fileformat.com/gis/gpx/) )
- Put result file (for example, 'orion.gpx') to separate folder (for example, **./gpx/**)
- Call script
  `python3 gpxtomap.py -d ./gpx/`
- Open *index.html*, containing map with all the info

Several files in folder can be processed at the same time, each of points and waypoints will contain file as source in description.

Слава Україні!

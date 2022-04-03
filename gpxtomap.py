
import logging
import argparse
import folium
from pathlib import Path
import random
from glob import glob 

import gpxpy
import gpxpy.gpx

UA_CENTER=[49.404321, 31.429246]
LINES_LIST=['red', 'blue', 'green', 'purple',  'darkred',
            'darkblue', 'darkgreen', 'cadetblue',
             'gray', 'black']
# bad for map
# 'lightblue', 'beige', 'white', 'orange', 'darkpurple', 'lightgray','lightred', 'pink', 'lightgreen',

def point_to_string(source, point):
    description = '<br><i>{}<i>'.format(point.description) if point.description else ''
    description += '<br>{}'.format(point.time.strftime('%c')) if point.time else ''

    return '<b>{}</b>{}<br><u>From: {}</u>'.format(point.name, description, source)


def compose_map(m, source_name, waypoints):

    # USUALLY EMPTY
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

    for waypoint in gpx.waypoints:
        icon_color = 'darkred' if waypoint.description else 'darkblue'
        icon_name = 'save' if waypoint.description else 'info'
        # icon_color = 'red' if waypoint.description else 'lightgreen'
        m.add_child(folium.Marker(
            [waypoint.latitude, waypoint.longitude],
            popup=point_to_string(source_name, waypoint),
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
        ))

    for route in gpx.routes:
        locations=[]
        for point in route.points:
            m.add_child(folium.Marker(
                [point.latitude, point.longitude],
                popup=point_to_string(source_name, point),
                icon=folium.DivIcon(icon_size=[5, 5], class_name='leaflet-div-icon')
            ))
            locations.append([point.latitude, point.longitude])
        if len(locations):
            random_color=random.choice(LINES_LIST)
            m.add_child(folium.vector_layers.PolyLine(
                locations,
                color=random_color,
                tooltip=route.name
            ))

    m.save('index.html')


if __name__ == '__main__':
    logging.basicConfig(
        filename='out.log',
        filemode='wt',
        level=logging.DEBUG
    )
    parser = argparse.ArgumentParser(
        description='Russian warship idi nahui'
    )

    parser.add_argument(
        '-d',
        metavar='directory',
        required=True,
        help='waylist and pointlist containing folder'
    )

    args = parser.parse_args()

    directory = Path(args.d).absolute()
    fnames = []
    for fname in glob( '{}/*.gpx'.format( directory )):
        print('found {}'.format(fname))
        fnames.append( fname )

    m = folium.Map(
        location=UA_CENTER,
        zoom_start=6
    )
    m.add_child(folium.LatLngPopup())

    for f in fnames:
        with open(f, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            compose_map(m, Path(f).stem, gpx)

# -*- coding: utf-8 -*-

import sys


class maidenhead(object):

    def to_grid(self,lat,lon):
        if lon>0:
            lon+= 180
        else:
            lon=180-lon
        if lat>0:
            lat += 90
        else:
            lat =90-lat

        grid=[None,None,None,None]
        v=int(lon/20)
        grid[0]=(chr(65+v))
        grid[2]=int((lon-v*20)/2)
        v=int(lat/10)
        grid[1]=(chr(65+v))
        grid[3]=



if __name__ == '__main__':
    mg=maidenhead()
    mg.to_grid(23.3,58.3)
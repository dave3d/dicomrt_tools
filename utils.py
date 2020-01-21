#! /usr/bin/env python

import re
import pydicom

def findROIByNumber(ds, num):
    """ find a ROI by its ID number """
    roi = ds.StructureSetROISequence

    for r in roi:
        if r.ROINumber == num:
            return r
    return None

def findROIByName(ds, name):
    """ find a ROI by its name """
    roi = ds.StructureSetROISequence

    for r in roi:
        if r.ROIName == name:
            return r
    return None

def findROIByPattern(ds, pattern):
    """ find all the regions whos names match a regular expression """

    results=[]
    roi = ds.StructureSetROISequence
    for r in roi:
      if re.match(pattern, r.ROIName):
        results.append(r)

    return results

def findRegions(ds, numbers=[], names=[], pattern=""):
    """ find all the regions by numbers, names or regular expressions """

    # if they passed in a string, convert it to a list
    if type(names)==str:
        names=[names]

    roi = ds.StructureSetROISequence
    results = []

    for r in roi:
        if len(pattern):
            if re.match(pattern, r.ROIName):
                results.append(r)
                continue
        if len(numbers):
            if r.ROINumber in numbers:
                results.append(r)
                continue
        if len(names):
            if r.ROIName in names:
                results.append(r)

    return results

def getContourSequenceData(cs):
    """ Get the number of points, lines, and starting indeces of each line of a contour sequence. """

    nlines = len(cs.ContourSequence)
    count = 0
    starts = []
    ncs = 0
    # Count up all the points in all the contours
    for c in cs.ContourSequence:
      starts.append(int(count/3))
      count = count + len(c.ContourData)
      ncs = ncs + 1

    npts = count/3
    #print(starts)

    return npts, nlines, starts


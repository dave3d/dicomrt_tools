#! /usr/bin/env python

import pydicom

def findROIByNumber(ds, num):
    roi = ds.StructureSetROISequence

    for r in roi:
        if r.ROINumber == num:
            return r
    return None

def findROIByName(ds, name):
    roi = ds.StructureSetROISequence

    for r in roi:
        if r.ROIName == name:
            return r
    return None

def outputContourSequence(ds, seqnum):
    ctrs = ds.ROIContourSequence
    seq = ctrs[seqnum]
    roi = findROIByNumber(ds, seq.ReferencedROINumber)
    out=[''] #lead with a blank line
    color = seq.ROIDisplayColor
    out.append("#color %d %d %d" % (color[0], color[1], color[2]))
    out.append("#name " + roi.ROIName)

    return out


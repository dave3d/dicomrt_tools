#! /usr/bin/env python

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


def contourSequence2VTK(cs=None, name="", color=[]):
    """ output a VTK polyline file from a contour sequence """
    out = ['# vtk DataFile Version 1.0']
    out.append('contour sequence %s' % name)
    out.append('ASCII')
    out.append('DATASET POLYDATA')

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

    out.append('POINTS %d float' % int(npts))

    # Output all the points in all the contours
    for c in cs.ContourSequence:
        i = 0
        n = len(c.ContourData)
        for i in range(0,n,3):
          out.append("%g %g %g" % (c.ContourData[i], c.ContourData[i+1], c.ContourData[i+2]))

    line_size = npts + 2*nlines
    out.append('')

    out.append('LINES %d %d' % (nlines, line_size))

    i = 0
    for c in cs.ContourSequence:
      n = int(len(c.ContourData)/3)
      # number of vertices in the contour
      out.append(str(n+1))
      verts = ""
      for j in range(n):
        verts = verts + " " + str(j+starts[i])
      # close the contour by repeating the first vertex
      verts = verts + " " + str(starts[i])
      out.append(verts)

      i=i+1
    return out


def outputContourSequenceByROINum(ds, seqnum):
    """ output a contour in Dave's .lns format """
    ctrs = ds.ROIContourSequence
    seq = ctrs[seqnum]
    roi = findROIByNumber(ds, seq.ReferencedROINumber)
    out=[''] #lead with a blank line
    color = seq.ROIDisplayColor
    out.append( "#color: %d %d %d" % (color[0], color[1], color[2]) )
    out.append( "#name: \'%s\'" % (roi.ROIName) )

    for c in seq.ContourSequence:
      n = len(c.ContourData)
      i = 0
      for i in range(0,n,3):
        out.append("%g %g %g" % (c.ContourData[i], c.ContourData[i+1], c.ContourData[i+2]))
      # close the contour
      out.append("%g %g %g" % (c.ContourData[0], c.ContourData[1], c.ContourData[2]))

      out.append('') # end each contour with a blank line

    return out

def outputContourSequenceByName(ds, name):
    """ find the contour by name, then call outputContourSequenceByROINum """
    ctrs = ds.ROIContourSequence
    seqnum = -1
    i = 0
    for seq in ctrs:
      roi = findROIByNumber(ds, seq.ReferencedROINumber)
      if roi.Name == name:
        seqnum = i
        break
      i = i+1

    if seqnum>=0:
      return outputContourSequenceByROINum(ds, seqnum)
    else:
      return []

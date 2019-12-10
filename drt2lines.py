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

def contourSequence2VTK(cs=None, name="", color=[]):
    """ output a VTK polyline file from a contour sequence """
    out = ['# vtk DataFile Version 1.0']
    out.append('contour sequence %s' % name)
    out.append('ASCII')
    out.append('DATASET POLYDATA')

    npts, nlines, starts = getContourSequenceData(cs)

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


def contourSequence2LNS(cs=None, name="", color=[]):
    """ output a contour in Dave's .lns format """
    out=[''] #lead with a blank line

    # convert 0-255 colors to 0-1.0
    scale = 1.0/255.0
    out.append( "#color: %g %g %g" % (scale*color[0], scale*color[1], scale*color[2]) )
    out.append( "#name: %s" % (name) )

    for c in cs.ContourSequence:
      n = len(c.ContourData)
      i = 0
      for i in range(0,n,3):
        out.append("%g %g %g" % (c.ContourData[i], c.ContourData[i+1], c.ContourData[i+2]))
      # close the contour
      out.append("%g %g %g" % (c.ContourData[0], c.ContourData[1], c.ContourData[2]))

      out.append('') # end each contour with a blank line

    return out


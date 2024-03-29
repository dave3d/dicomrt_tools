#! /usr/bin/env python

import utils


def contourSequence2VTK(cs=None, name="", color=[], verbose=False):
    """ output a VTK polyline file from a contour sequence """
    out = ['# vtk DataFile Version 1.0']
    out.append('contour sequence %s' % name)
    out.append('ASCII')
    out.append('DATASET POLYDATA')

    npts, nlines, starts = utils.getContourSequenceData(cs)

    if verbose:
        print("%d points, %d lines " % (npts, nlines))

    out.append('POINTS %d float' % int(npts))

    # Output all the points in all the contours
    for c in cs.ContourSequence:
        i = 0
        n = len(c.ContourData)
        for i in range(0, n, 3):
            out.append("%g %g %g" % (c.ContourData[i], c.ContourData[i + 1],
                                     c.ContourData[i + 2]))

    line_size = npts + 2 * nlines
    out.append('')

    out.append('LINES %d %d' % (nlines, line_size))

    i = 0
    for c in cs.ContourSequence:
        n = int(len(c.ContourData) / 3)
        # number of vertices in the contour
        out.append(str(n + 1))
        verts = ""
        for j in range(n):
            verts = verts + " " + str(j + starts[i])
        # close the contour by repeating the first vertex
        verts = verts + " " + str(starts[i])
        out.append(verts)
        if verbose:
            print("contour %d has %d points" % (i, n + 1))

        i = i + 1
    return out


def contourSequence2LNS(cs=None, name="", color=[], verbose=False):
    """ output a contour in Dave's .lns format """
    out = ['']  # lead with a blank line

    bound_min = [1e32, 1e32, 1e32]
    bound_max = [-1e32, -1e32, -1e32]

    # convert 0-255 colors to 0-1.0
    if len(color) == 3:
        scale = 1.0 / 255.0
        out.append("#color: %g %g %g" % (scale * color[0], scale * color[1],
                                         scale * color[2]))
    out.append("#name: %s" % (name))

    count = 0
    for c in cs.ContourSequence:
        n = len(c.ContourData)
        i = 0
        for i in range(0, n, 3):
            pt = [c.ContourData[i], c.ContourData[i + 1], c.ContourData[i + 2]]
            out.append("%g %g %g" % (pt[0], pt[1], pt[2]))
            for j in range(3):
                if pt[j] < bound_min[j]:
                    bound_min[j] = pt[j]
                if pt[j] > bound_max[j]:
                    bound_max[j] = pt[j]

        # close the contour
        out.append("%g %g %g" % (c.ContourData[0], c.ContourData[1],
                                 c.ContourData[2]))
        if verbose:
            print("%d points in contour %d" % (n + 1, count))
        count = count + 1

        out.append('')  # end each contour with a blank line

    print("Contour bounds")
    print("    min: ", bound_min[0], bound_min[1], bound_min[2])
    print("    max: ", bound_max[0], bound_max[1], bound_max[2])

    return out

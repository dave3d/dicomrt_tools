import utils

has_vtk = False
try:
    import vtk

    has_vtk = True
except ImportError:
    pass


def contourSequence2PolyLines(cs):
    """ Create a set of VTK polylines from a contour sequence """

    if not has_vtk:
        print("Error: VTK package not found")
        return

    npts, nlines, starts = utils.getContourSequenceData(cs)

    points = vtk.vtkPoints()

    # add all the points of all the contours
    for c in cs.ContourSequence:
        i = 0
        n = len(c.ContourData)
        for i in range(0, n, 3):
            pt = [c.ContourData[i], c.ContourData[i + 1], c.ContourData[i + 2]]
            points.InsertNextPoint(pt)

    lines = vtk.vtkCellArray()

    # create the VTK PolyLines for the contours
    i = 0
    for c in cs.ContourSequence:
        n = int(len(c.ContourData) / 3)
        line = vtk.vtkPolyLine()
        line.GetPointIds().SetNumberOfIds(n + 1)
        for j in range(n):
            line.GetPointIds().SetId(j, j + starts[i])
        line.GetPointIds().SetId(n, starts[i])
        lines.InsertNextCell(line)
        i = i + 1

    linesPolyData = vtk.vtkPolyData()
    linesPolyData.SetPoints(points)
    linesPolyData.SetLines(lines)

    return linesPolyData


def contourSequence2Image(cs, output_type='meta', name=""):
    print("I should probably do something some day")

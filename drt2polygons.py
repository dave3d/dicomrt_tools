
import drt2polylines

has_vtk = False
try:
    import vtk

    has_vtk = True
except ImportError:
    pass


def contourSequence2Polygons(cs):
    linesPolyData = drt2polylines.contourSequence2PolyLines(cs)

    f = vtk.vtkVoxelContoursToSurfaceFilter()

    f.SetInputData(linesPolyData)
    f.Update()

    return f.GetOutputDataObject(0)



has_vtk = False
try:
  import vtk
  has_vtk=True
except ImportError:
  pass

from drt2polylines import *


def  contourSequence2Polygons(cs):

    linesPolyData = contourSequence2PolyLines(cs)

    f = vtk.vtkVoxelContoursToSurfaceFilter()

    f.SetInputData(linesPolyData)
    f.Update()

    return f.GetOutputDataObject(0)

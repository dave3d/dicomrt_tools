
import sys
import vtk
import traceback

def writeVTKMesh(mesh, name, binary=True):
    """Write a VTK mesh file."""
    try:
        writer = vtk.vtkPolyDataWriter()
        writer.SetInputData(mesh)
        if binary:
            writer.SetFileTypeToBinary()
        writer.SetFileName(name)
        writer.Write()
        print("Output mesh:", name)
        writer = None
    except BaseException:
        print("VTK mesh writer failed")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    return None



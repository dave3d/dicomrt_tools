
import math
import vtk
import drt2polylines


def contourSequence2Volume(cs, spacing=[1, 1, 1]):
    polylines = drt2polylines.contourSequence2PolyLines(cs)

    stencil = vtk.vtkPolyDataToImageStencil()
    stencil.SetInputData(polylines)

    bounds = polylines.GetBounds()
    i = 0
    bounds2 = []
    for x in bounds:
        if i & 1:
            y = math.ceil(x) + 1
        else:
            y = math.floor(x) - 1
        bounds2.append(y)
        i = i + 1

    stencil.SetOutputWholeExtent(bounds2[0], bounds2[1], bounds2[2],
                                 bounds2[3], bounds2[4], bounds2[5])

    stencil.SetOutputSpacing(spacing[0], spacing[1], spacing[2])
    stencil.Update()

    sten2img = vtk.vtkImageStencilToImage()
    sten2img.SetInputConnection(stencil.GetOutputPort())
    sten2img.SetOutsideValue(0)
    sten2img.SetInsideValue(255)
    sten2img.Update()
    vtkimg = sten2img.GetOutput()
    return vtkimg

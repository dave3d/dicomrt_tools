
import vtk

def view(pdlist, colorlist):

    colors = vtk.vtkNamedColors()

    # Setup render window, renderer, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Contour Sequence View")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderer.SetBackground(colors.GetColor3d("DarkSlateBlue"))

    i = 0
    for pd in pdlist:
      mapper = vtk.vtkPolyDataMapper()
      mapper.SetInputData(pd)

      actor = vtk.vtkActor()
      actor.SetMapper(mapper)
      try:
        color = colorlist[i]
        if len(color) < 3:
          raise
      except:
        color = [1.0, 1.0, 1.0]
      actor.GetProperty().SetColor(color)
      renderer.AddActor(actor)

      i=i+1

    renderWindow.SetSize(2000,1500)
    renderWindow.Render()
    renderWindowInteractor.Start()


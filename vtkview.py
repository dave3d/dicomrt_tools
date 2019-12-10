
import vtk

def view(pdlist):

    colors = vtk.vtkNamedColors()

    # Setup render window, renderer, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Contour Sequence View")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderer.SetBackground(colors.GetColor3d("DarkOliveGreen"))

    for pd in pdlist:
      mapper = vtk.vtkPolyDataMapper()
      mapper.SetInputData(pd)

      actor = vtk.vtkActor()
      actor.SetMapper(mapper)
      actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
      renderer.AddActor(actor)

    renderWindow.Render()
    renderWindowInteractor.Start()


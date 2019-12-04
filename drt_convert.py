#! /usr/bin/env python

import sys, getopt
import pydicom
import dicomrt_tools as drt


def OutputContoursAsLines(ds, contour_names=[], verbose=False):

  contours = ds.ROIContourSequence
  print (len(contours), "contours")
  print(dir(contours[0]))

  i = 0

  for c in contours:
    r = drt.findROIByNumber(ds, c.ReferencedROINumber)
    if len(contour_names) and not(r.ROIName in contour_names):
      if verbose:
        print ("Skipping ", r.ROIName)
      i=i+1
      continue
    print ()
    print("Contour Sequence:", i)
    print("color:", c.ROIDisplayColor)
    print ("ROI number:", c.ReferencedROINumber)
    print ("ROI name:", r.ROIName)
    print("# of contours:", len(c.ContourSequence))

    outname = r.ROIName.replace(' ', '_') + ".lns"
    outfile = open(outname, "w")
    print(outname)

    out = drt.outputContourSequenceByROINum(ds, i)
    #print(out)
    for x in out:
      print(x, file=outfile)
    i=i+1

    outfile.close()


def OutputContoursAsVTK(ds, contour_names=[], verbose=False):
  contours = ds.ROIContourSequence
  print (len(contours), "contours")
  print(dir(contours[0]))

  i = 0
  print (contour_names)

  for c in contours:
    r = drt.findROIByNumber(ds, c.ReferencedROINumber)
    if len(contour_names) and not(r.ROIName in contour_names):
      if verbose:
        print ("Skipping ", r.ROIName)
      i=i+1
      continue
    print ()
    print("Contour Sequence:", i)
    print("color:", c.ROIDisplayColor)
    print ("ROI number:", c.ReferencedROINumber)
    print ("ROI name:", r.ROIName)
    print("# of contours:", len(c.ContourSequence))

    outname = r.ROIName.replace(' ', '_') + ".vtk"
    outfile = open(outname, "w")
    print(outname)

    out = drt.contourSequence2VTK(c, r.ROIName, c.ROIDisplayColor)
    #print(out)
    for x in out:
      print(x, file=outfile)
    i=i+1

    outfile.close()


def OutputContoursAsMetaIO(ds, contour_names=[], verbose=False):
  print( "This don't do nuttin' yet")


def usage():
  print ( )
  print ( "Usage: drt_convert [options] input_dicom_rt_file" )
  print ( )
  print ( "   -h, --help     This help message" )
  print ( "   -V, --verbose  Verbose messages" )
  print ( "   -l, --line     Output line files" )
  print ( "   -v, --vtk      Output VTK polyline files" )
  print ( "   -m, --meta     Output MetaIO volume images" )
  print ( )



def parseArgs():

  settings = {}
  cn = []
  settings['contour_names'] = cn
  settings['verbose'] = False
  settings['output_type'] = 'line'

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hVlvmc:",
      ["help", "verbose", "line", "vtk", "meta", "contour="] )
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(1)

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit(0)
    elif o in ("-V", "--verbose"):
      settings['verbose'] = True
    elif o in ("-l", "--line"):
      output_type = 'line'
      settings['output_type'] = 'line'
    elif o in ("-v", "--vtk"):
      output_type = 'vtk'
      settings['output_type'] = 'vtk'
    elif o in ("-m", "--meta"):
      print("Meta!")
      settings['output_type'] = 'meta'
      output_type = 'meta'
    elif o in ("-c", "--contour"):
      cn.append(a)
    else:
      assert False, "unhandled options"

  print(args)
  print(settings)
  return args, settings



def main():

  infiles, settings = parseArgs()

  output_type = settings['output_type']
  contour_names = settings['contour_names']

  if len(infiles) == 0:
    infiles = ["1041312_StrctrSets.dcm"]
  print (infiles)
  for infile in infiles:
    print(infile)

    ds = pydicom.read_file(infile, force=True)
    print("output type:", output_type)

    if output_type == 'line':
      OutputContoursAsLines(ds, contour_names, settings['verbose'])
    elif output_type == 'vtk':
      OutputContoursAsVTK(ds, contour_names, settings['verbose'])
    elif output_type == 'meta':
      OutputContoursAsMetaIO(ds, contour_names, settings['verbose'])



if __name__ == "__main__":

  main()

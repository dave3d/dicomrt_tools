#! /usr/bin/env python

import sys, getopt
import pydicom
import dicomrt_tools as drt


infiles = []
contour_names = []
output_type = 'line'

def OutputContoursAsLines(ds, contour_names):

  contours = ds.ROIContourSequence
  print (len(contours), "contours")
  print(dir(contours[0]))

  i = 0

  for c in contours:
    r = drt.findROIByNumber(ds, c.ReferencedROINumber)
    if len(contour_names) and not(r.ROIName in contour_names):
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


def OutputContoursAsVTK(ds, contour_names):
  contours = ds.ROIContourSequence
  print (len(contours), "contours")
  print(dir(contours[0]))

  i = 0
  print (contour_names)

  for c in contours:
    r = drt.findROIByNumber(ds, c.ReferencedROINumber)
    if len(contour_names) and not(r.ROIName in contour_names):
      print ("ROI name:", r.ROIName)
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

def usage():
  print ( )
  print ( "Usage: drt_convert [options] input_dicom_rt_file" )
  print ( )
  print ( "   -h, --help     This help message" )
  print ( "   -l, --line     Output line files" )
  print ( "   -v, --vtk      Output VTK polyline files" )
  print ( "   -m, --meta     Output MetaIO volume images" )
  print ( )



def parseArgs():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hlvmc:",
      ["help", "line", "vtk", "meta", "contour="] )
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(1)

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit(0)
    elif o in ("-l", "--line"):
      output_type = 'line'
    elif o in ("-v", "--vtk"):
      output_type = 'vtk'
    elif o in ("-m", "--meta"):
      print("Meta!")
      output_type = 'meta'
    elif o in ("-c", "--contour"):
      contour_names.append(a)
    else:
      assert False, "unhandled options"

  print(args)
  return args



def main():
  infiles = parseArgs()
  if len(infiles) == 0:
    infiles = ["1041312_StrctrSets.dcm"]
  print (infiles)
  for infile in infiles:
    print(infile)

    ds = pydicom.read_file(infile, force=True)
    print("output type:", output_type)

    if output_type == 'line':
      print("output type: line")
      OutputContoursAsLines(ds, contour_names)
    elif output_type == 'vtk':
      print("output type: vtk")
      OutputContoursAsVTK(ds, contour_names)
      print("output type: meta")
    elif output_type == 'meta':
      print("Not yet implemented, Dude")



if __name__ == "__main__":

  main()

#! /usr/bin/env python

import sys
import pydicom
import dicomrt_tools as drt

if (len(sys.argv) > 1):
  infiles = sys.argv[1:]
else:
  # my test file
  infiles = ["1041312_StrctrSets.dcm"]

print(infiles)

contour_names = {"25 Gy LI"}

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


for infile in infiles:
  print(infile)

  ds = pydicom.read_file(infile, force=True)

  OutputContoursAsLines(ds, contour_names)
#  OutputContoursAsVTK(ds, contour_names)

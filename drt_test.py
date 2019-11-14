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

for infile in infiles:
  print(infile)

  ds = pydicom.read_file(infile, force=True)

  contours = ds.ROIContourSequence
  print (len(contours), "contours")
  print(dir(contours[0]))

  i = 0

  for c in contours:
    print ()
    print("Contour Sequence:", i)
    print("color:", c.ROIDisplayColor)
    print ("ROI number:", c.ReferencedROINumber)
    r = drt.findROIByNumber(ds, c.ReferencedROINumber)
    print ("ROI name:", r.ROIName)
    print("# of contours:", len(c.ContourSequence))

    out = drt.outputContourSequence(ds, i)
    print(out)
    i=i+1


#! /usr/bin/env python

import getopt
import os
import sys

import pydicom

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.append(root_folder)

import drt2files  # noqa: E402
import drt2polylines  # noqa: E402
import vtkview  # noqa: E402
import utils  # noqa: E402


def OutputContours(ds, output_type='line', contour_names=[], verbose=False):
    try:
        contour_sequences = ds.ROIContourSequence
    except BaseException:
        print("Uh-oh: couldn't find ROIContourSequence")
        print(dir(ds))
        return

    print(len(contour_sequences), "contour sequences")

    i = 0

    for cs in contour_sequences:
        r = utils.findROIByNumber(ds, cs.ReferencedROINumber)
        if len(contour_names) and not (r.ROIName in contour_names):
            if verbose:
                print("Skipping ", r.ROIName)
            i = i + 1
            continue
        print()
        print("Contour Sequence:", i)
        print("color:", cs.ROIDisplayColor)
        print("ROI number:", cs.ReferencedROINumber)
        print("ROI name:", r.ROIName)
        print("# of contours:", len(cs.ContourSequence))

        if output_type == 'line':
            outname = r.ROIName.replace(' ', '_') + ".lns"
            out = drt2files.contourSequence2LNS(cs, r.ROIName,
                                                cs.ROIDisplayColor, verbose)
        elif output_type == 'vtk':
            outname = r.ROIName.replace(' ', '_') + ".vtk"
            out = drt2files.contourSequence2VTK(cs, r.ROIName,
                                                cs.ROIDisplayColor, verbose)

        print(outname)
        outfile = open(outname, "w")
        # print(out)
        for x in out:
            print(x, file=outfile)
        i = i + 1

        outfile.close()


def OutputContoursAsImages(ds, contour_names=[], verbose=False):
    contour_sequences = ds.ROIContourSequence
    print(len(contour_sequences), "contour sequences")

    i = 0

    for cs in contour_sequences:
        r = utils.findROIByNumber(ds, cs.ReferencedROINumber)
        if len(contour_names) and not (r.ROIName in contour_names):
            if verbose:
                print("Skipping ", r.ROIName)
            i = i + 1
            continue
        print()
        print("Contour Sequence:", i)
        print("color:", cs.ROIDisplayColor)
        print("ROI number:", cs.ReferencedROINumber)
        print("ROI name:", r.ROIName)
        print("# of contours:", len(cs.ContourSequence))

        drt2polylines.contourSequence2Image(cs, 'meta', r.ROIName)


def displayContours(ds, contour_names=[], verbose=False):
    contour_sequences = ds.ROIContourSequence
    print(len(contour_sequences), "contour sequences")

    i = 0
    pdlist = []
    colorlist = []

    for cs in contour_sequences:
        r = utils.findROIByNumber(ds, cs.ReferencedROINumber)
        if len(contour_names) and not (r.ROIName in contour_names):
            if verbose:
                print("Skipping ", r.ROIName)
            i = i + 1
            continue
        print()
        print("Contour Sequence:", i)
        print("color:", cs.ROIDisplayColor)
        print("ROI number:", cs.ReferencedROINumber)
        print("ROI name:", r.ROIName)
        print("# of contours:", len(cs.ContourSequence))

        pdlist.append(drt2polylines.contourSequence2PolyLines(cs))
        color = [float(x) / 255.0 for x in cs.ROIDisplayColor]

        colorlist.append(color)
    vtkview.view(pdlist, colorlist)


def usage():
    print()
    print("Usage: drt_convert [options] input_dicom_rt_file")
    print()
    print("   -h, --help     This help message")
    print("   -V, --verbose  Verbose messages")
    print("   -l, --line     Output line files")
    print("   -v, --vtk      Output VTK polyline files")
    print("   -m, --meta     Output MetaIO volume images")
    print("   -d, --display  Display contours (using VTK)")
    print("   -c name, --contour name     Select contour by name",
          "(multiple names allowed)")
    print("   -r 'regex'     Select contour by regular expression")
    print()


def parseArgs():
    settings = {}
    cn = []
    settings['contour_names'] = cn
    settings['verbose'] = False
    settings['display'] = False
    settings['output_type'] = 'line'
    settings['regex'] = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVlvmdc:r:",
                                   ["help", "verbose", "line", "vtk", "meta",
                                    "display", "contour=", "regex="])
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
            settings['output_type'] = 'line'
        elif o in ("-v", "--vtk"):
            settings['output_type'] = 'vtk'
        elif o in ("-m", "--meta"):
            settings['output_type'] = 'meta'
        elif o in ("-c", "--contour"):
            cn.append(a)
        elif o in ("-r", "--regex"):
            settings['regex'] = a
        elif o in ("-d", "--display"):
            settings['display'] = True
        else:
            assert False, "unhandled options"

    print(args)
    print(settings)
    return args, settings


def main():
    infiles, settings = parseArgs()

    output_type = settings['output_type']

    if len(infiles) == 0:
        infiles = ["1041312_StrctrSets.dcm"]
    print(infiles)
    for infile in infiles:
        print(infile)
        contour_names = settings['contour_names']

        ds = pydicom.read_file(infile, force=True)
        print("output type:", output_type)

        if settings['display']:
            displayContours(ds, contour_names, settings['verbose'])
        else:

            if output_type == 'meta':
                OutputContoursAsImages(ds, contour_names, settings['verbose'])
            else:
                OutputContours(ds, output_type, contour_names,
                               settings['verbose'])


if __name__ == "__main__":
    main()

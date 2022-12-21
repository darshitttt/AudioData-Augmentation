import os
import subprocess
import sys

def change_format(*args):
    outfile0 =''
    # Splitting the filename to get the same name as the original one
    out = os.path.splitext(args[0][0])
    outfile, dummy = out
    outfile0 += outfile
    outfile = outfile.split('/')
    outfile.insert(7, 'formatted')
    outfile0 = '/'.join(outfile)

    outfile0 += '.wav'


    #print("Input file looks like this : ", outfile)
    #print("Output file looks like this : ", outfile0)
    #print('outfile0:', outfile0)
    # Command list to be passed to the subprocess.call argument
    list = ['sox', args[0][0], '-b', '16', '-e', 'signed-integer', outfile0]

    #print(list)
    # Subprocess call to convert the given audio format to wav
    subprocess.call(list)

    return 1



path = sys.argv
fn = sys.argv[-1:]

change_format(fn)

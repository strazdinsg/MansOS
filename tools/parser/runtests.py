#!/usr/bin/env python

import main, sys, os

testFileDir = 'tests'
architecture = 'testarch'
#architecture = 'telosb'
targetOS = 'mansos'
outputDirName = "build"

def runTest(sourceFileName):
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    outputFileName = outputDirName + '/' + os.path.basename(sourceFileName[:-2]) + 'c'

    sys.argv = ["./main.py", "-e", "-a", architecture, "-t", targetOS, "-o", outputFileName, sourceFileName]

    try:
        main.main()
    except Exception:
        pass

    # prepend output with the test script
    with open(outputFileName, 'r+') as outputFile:
        contents = outputFile.read()
        outputFile.seek(os.SEEK_SET, 0)
        outputFile.truncate()
        outputFile.write("/*\n")
        with open(sourceFileName, 'r') as sourceFile:
            outputFile.write(sourceFile.read())
        outputFile.write("*/\n\n")
        outputFile.write(contents)

def runTests():
    numTests = 0
    files = os.listdir(testFileDir)
    files.sort()
    for f in files:
        if len(f) < 3 or f[len(f) - 3:] != '.sl': continue
        sourceFileName = os.path.join(testFileDir, f)
        print "\nprocessing " + sourceFileName + "..."
        runTest(sourceFileName)
        numTests += 1
        # break ###
    print numTests, "tests successfully executed"

if __name__ == '__main__':
    runTests()

#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot
import instrument


if __name__ == "__main__":


    # Initialize our scope
    test = instrument.TekScope1000("/dev/usbtmc2")

    # Stop data acquisition
    test.write("ACQ:STATE STOP")

    # Set data width to 2 for better resolution
    test.write("DATA:WIDTH 2")

    # Set data format to binary, zero is center-frame and big endian
    test.write("DATA:ENCD SRI")

    # Find out what is displayed on the scope:
    # "wfms" is a string with 1 or 0 for CH1,CH2,MATH,REFA,REFB
    test.write("SELECT?")
    wfms = test.read(20)
    # parse into array of characters
    wfms = wfms.strip().split(";")

    if wfms[0]=="1":
        test.write("DATA:SOURCE CH1")
        test.write("CURV?")
        rawdata = test.read(125000)
        ch1data = numpy.frombuffer(rawdata,offset=3+int(rawdata[1]),count = 10000)

    if wfms[1]=="1":
        test.write("DATA:SOURCE CH2")
        test.write("CURV?")
        rawdata = test.read(125000)
        ch2data = numpy.frombuffer(rawdata,offset=3+int(rawdata[1]),count = 10000)

    if wfms[3]=="1":
        test.write("DATA:SOURCE CH3")
        test.write("CURV?")
        rawdata = test.read(125000)
        ch3data = numpy.frombuffer(rawdata,offset=3+int(rawdata[1]),count = 10000)

    if wfms[4]=="1":
        test.write("DATA:SOURCE CH4")
        test.write("CURV?")
        rawdata = test.read(125000)
        ch4data = numpy.frombuffer(rawdata,offset=3+int(rawdata[1]),count = 10000)

    if wfms[5]=="1":
        test.write("DATA:SOURCE REFB")
        test.write("CURV?")
        rawdata = test.read(125000)
        refBdata = numpy.frombuffer(rawdata,offset=3+int(rawdata[1]),count = 10000)

    # Get the timescale
    test.write("HORIZONTAL:MAIN:SCALE?")
    timescale = float(test.read(20))

    # Get the timescale offset
    test.write("HORIZONTAL:MAIN:POSITION?")
    timeoffset = float(test.read(20))

    # Get the length of the horizontal record
    test.write("HORIZONTAL:RECORDLENGTH?")
    #time_size = int(test.read(30))
    time_size = 10000

    time = numpy.arange(0,timescale*10,timescale*10/time_size)
    # Start data acquisition again, and put the scope back in local mode
    #test.write("ACQ:STATE RUN")
    #test.write("UNLOCK ALL")

    # Number of current available channels
    numPlots = 2

    # Plot the data
    if wfms[0]=="1":
        plot.subplot(numPlots,1,1)
        plot.plot(time,ch1data)
        plot.title("Channel 1")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (S)")
    if wfms[1]=="1":
        plot.subplot(numPlots,1,2)
        plot.plot(time,ch2data)
        plot.title("Channel 2")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (S)")
    if wfms[2]=="1":
        plot.subplot(numPlots,1,3)
        plot.plot(ch3data)
        plot.title("Channel 3")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (S)")
    if wfms[3]=="1":
        plot.subplot(numPlots,1,4)
        plot.plot(ch4data)
        plot.title("Channel 4")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (S)")


    #plot.xlim(time[0], time[599]
    plot.show()
    #plot.savefig("test.png")


class Error_Program:
    def __init__(self):
        pass

    # ==========  ERROR PROG  ====================================+
    def error_prog(self, kode):
        if kode == 0:
            return " EC_Okay 0 Execution without any error."
        elif kode == 1:
            return " EC_NoRequest 1	Nothing was requested (no parameters), and nothing was done"
        elif kode == 20:
            return "EC_Memory 20 Not enough main memory available."
        elif kode == 21:
            return "EC_System 21 System problem e.g. needed DLL file missing."
        elif kode == 22:
            return "EC_Phys 22 Problem with physical interface – e.g. COM2 not installed."
        elif kode == 30:
            return "EC_Arg 30 The call specified illegal program arguments."
        elif kode == 31:
            return "EC_FilFind 31 A specified input file is not available."
        elif kode == 32:
            return "EC_FilForm 32 An input file does not have the required format."
        elif kode == 33:
            return "EC_FilVer 33 An input file has an incompatible file version."
        elif kode == 34:
            return "EC_FilWrite	34 An output file could not be opened or wrote on to."
        elif kode == 40:
            return "EC_NoConn 40 Connection to the device failed."
        elif kode == 41:
            return "EC_Comm 41 Error during communication or communication abort."
        elif kode == 42:
            return "EC_Timeout 42 Communication timeout (caused by a communications problem or device failure)."
        elif kode == 50:
            return "EC_Intern 50 Internal error – should not occur."
        elif kode == 51:
            return "EC_IllDev 51 Illegal device behavior – maybe caused by communications failure."
        elif kode == 52:
            return "EC_DevSW 52	The necessary software is not available on the device."
        elif kode == 53:
            return "EC_DevVer 53 The device uses an incompatible software version."
        elif kode == 54:
            return "EC_NoData 54 The device does not contain any data of the requested kind."
        elif kode == 55:
            return "EC_Conf 55 The device does not contain a valid configuration."
        elif kode == 56:
            return "EC_Compile 56 During compilation of the configuration an error occurred."
        else:
            return "NOT kod ERROR."

#####################################

# EC_Okay 	    0 	Execution without any error.
# EC_NoRequest 	1 	Nothing was requested (no parameters), and nothing was done.
# EC_Memory 	20 	Not enough main memory available.
# EC_System 	21 	System problem e.g. needed DLL file missing.
# EC_Phys 	    22 	Problem with physical interface – e.g. COM2 not installed.
# EC_Arg 	    30 	The call specified illegal program arguments.
# EC_FilFind 	31 	A specified input file is not available.
# EC_FilForm 	32 	An input file does not have the required format.
# EC_FilVer 	33 	An input file has an incompatible file version.
# EC_FilWrite 	34 	An output file could not be opened or wrote on to.
# EC_NoConn 	40 	Connection to the device failed.
# EC_Comm 	    41 	Error during communication or communication abort.
# EC_Timeout 	42 	Communication timeout (caused by a communications problem or device failure).
# EC_Intern 	50 	Internal error – should not occur.
# EC_IllDev 	51 	Illegal device behavior – maybe caused by communications failure.
# EC_DevSW 	    52 	The necessary software is not available on the device.
# EC_DevVer 	53 	The device uses an incompatible software version.
# EC_NoData 	54 	The device does not contain any data of the requested kind.
# EC_Conf 	    55 	The device does not contain a valid configuration.
# EC_Compile 	56 	During compilation of the configuration an error occurred.


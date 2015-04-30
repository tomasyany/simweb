"""This class manages all the outputs."""

class ConsolePrinter(object):

    @staticmethod
    def console(time, event):
        """Prints directly on the console."""
        
        print ("--------------------------------\n")
        print ("Time = "+str(time)+" - "+ event)



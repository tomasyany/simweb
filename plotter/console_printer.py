"""This class manages all the outputs."""

class ConsolePrinter(object):

    @staticmethod
    def step(time, event):
        """Prints directly on the console."""
        
        print ("--------------------------------\n")
        print ("Time = "+str(time)+" - "+ event)

    @staticmethod
    def welcome():
        """Prints welcome message."""
        
        space = "                       "
        lines = "----------------------------------"+\
        "------------------------------------------------" 

        print ('\n\n'+lines)

        print (space+"Welcome to the TRUCK SIMULATOR\n"+
                "A simulation sofware by Oscar Flores, Manuel Pérez, "+ 
                "Tomás Yany and Roberto Zúñiga.")

        print (lines+'\n\n')

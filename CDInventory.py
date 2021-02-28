#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# CBuffalow, 2021-Feb-19, Added functions (process_cd_data, process_delete, write_file, 
#   get_cd_data), added uppercase functionality to menu for better readability, 
#   adjusted formatting, added program header
# CBuffalow, 2021-Feb-20, Added calculcate_cd_id function, adjusted 
#    process_cd_data & get_cd_data functions, revised comments
# CBuffalow, 2021-Feb-25, Changed permanent data storage from txt to dat.
# CBuffalow, 2021-Feb-26, Revised cd_id program to generate from current inventory
#   instead of permament storage, added error handling around write, read, and input functions
# CBuffalow, 2021-Feb-27, Added additional error handling around program
#------------------------------------------#

# -- MODULES -- #
import pickle

# -- DATA -- #
#Global Variables
strChoice = '' # user input (string)
strYesNo = '' # user input for yes/no question (string)
indID = -1 # ID number of CD (integer)
strTitle = '' # user input (string)
strArtist = '' # user input (string)
lstTbl = []  # table to hold data (list of dictionaries)
dicRow = {}  # row of data (dictionary)
strFileName = 'CDInventory.dat'  # data storage file
intIDDel = '' # user selected ID to delete (integer)
intRowNr = '' # index of row to be deleted (integer)
blnCDRemoved = "False" # flag if desired CD found (Boolean)


# -- PROCESSING -- #
class DataProcessor:
    """Processing data within program's current runtime."""

    @staticmethod
    def calculate_cd_id(table):
        """Function to determine the appropriate ID number for the CD.

        The function finds the last row of data in the current inventory and reports 
        the ID number used in that row.  The function then adds 1 to the ID number
        to be used on the next CD.

        Args:
            table (list of dict): 2D data structure (list of dicts)

        Returns:
            cd_id (int): ID number for the CD
        """

        try: 
            tableIndex = len(table) -1
            cd_id = int(table[tableIndex]['ID']) + 1 #should already be an integer, but just in case...
        except IndexError:  #the IndexError will occur any time the table is empty & is not alarming, so simply assigning cd_id = 1 (1st entry)
            cd_id = 1
        except Exception as e: #in case something weird happens - still handling by assigning cd_id = 1
            cd_id = 1
            print('There has been a ', type(e), ' error. The next ID number will be 1.')
        finally:
            return cd_id



    @staticmethod
    def process_cd_data(cd_id, cd_title, cd_artist):
        """Function that takes user input about CD and formats data into a dictionary.

        Keys are "ID", 'Title', and 'Artist' for each dictionary and the values are assigned
        from cd_id, cd_title, and cd_artist, respectively.

        Args:
            cd_id (int): ID of CD, generated by program
            cd_title (str): name of CD, provided by user
            cd_artist (str): name of artist, provided by user

        Returns:
            cd_info (dictionary): cd_id, cd_title, and cd_artist contained within a single dictionary
        """
        try:
            cd_info = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        except Exception as e: #in case something weird happens
            cd_info = {'ID': 0, 'Title': 'NA', 'Artist': 'NA'}
            print('There has been a ', type(e), ' error. A generic dictionary has been created instead.')
        finally:
            return cd_info



    @staticmethod
    def process_delete(cd_to_delete, table):
        """Function that processes which row index needs to be deleted based upon input from user.

        For each dictionary, the function determines if the key:value pair in that row/dictionary 
        with the key of "ID" has the desired ID number for its value.  If yes, row_number stops counting
        at that row and CD_found is set to 'True'.

        Args:
            cd_to_delete (int): ID number of CD that user wants to delete
            table (list of dicts): 2D data structure (list of dicts) that holds data during runtime

        Returns:
            row_number (int): counter of rows (stops on row if desired CD found, otherwise returns index of last row)
            CD_found (Boolean): flag that states if desired CD found (True = yes, False = no)
        """
        row_number = -1
        CD_found = False
        try:
            for row in table:
                row_number += 1
                if row['ID'] == cd_to_delete:
                    CD_found = True
                    break
        except Exception as e: #in case something weird happens
            print('There has been a ', type(e), ' error. No CD will be deleted.')
            row_number = -1 #doesn't really matter what this value is when CD_found is False
            CD_found = False #CD_found as false will trigger the if/else in main script to NOT delete CD
        finally:
            return row_number, CD_found



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to read data from a .dat file using pickling.

        Function checks to make sure specified txt file exists.  If yes, it
        continues by reading the data from .dat file and saving it to 'table' 
        using pickling. If no, an empty list is assigned to 'Table'.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table (list of dict): 2D data structure (list of dicts)
        """
        try: 
            with open(file_name, 'rb') as objFile:
                table = pickle.load(objFile)
        except FileNotFoundError:
            print('File not found. Inventory is still empty.')
            table = []
        except Exception as e:
            print('There has been a ', type(e), ' error with the read process. Inventory is still empty.')
            table = []
        return table



    @staticmethod
    def write_file(file_name, table):
        """Function to write data from current runtime to a .dat file using pickling.

        The data from 'table' is saved to the designated .dat file using
        pickling.

        Args:
            file_name (string): name of file used to write data to
            table (list of dicts): 2D data structure (list of dicts) that holds data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'wb') as objFile:
                pickle.dump(table, objFile)
        except Exception as e: #if there is a general error with the save process
            print('There has been a ', type(e), ' error with the save process. File not saved.')


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user.


        Args:
            None.

        Returns:
            None.
        """
        print('\n')
        print(' MENU '.center(30,'-'))
        print('[L] Load Inventory from file\n[A] Add CD\n[I] Display Current Inventory')
        print('[D] Delete CD from Inventory\n[S] Save Inventory to file\n[X] Exit')
        print('-'*30)
        print('\n')



    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.


        Args:
            None.

        Returns:
            choice (string): an upper case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['L', 'A', 'I', 'D', 'S', 'X', 'l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [L, A, I, D, S or X]: ').lower().strip()
        print()  # Add extra space for layout
        return choice



    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n')
        print(' The Current Inventory: '.center(60,'='))
        print('{:<10}{:<25}{:<25}'.format('ID', 'CD Title', 'Artist'))
        print('-'*60)
        for row in table:
            print('{:<10}{:<25}{:<25}'.format(*row.values()))
        print('='*60)



    @staticmethod
    def get_cd_data():
        """Collects information about CD from user.

        Asks user to input the name of the CD and the artist of the CD.

        Args:
            None

        Returns:
            cd_title (str): name of CD, provided by user
            cd_artist (str): name of artist, provided by user

        """

        try: 
            cd_title = input('What is the CD\'s title? ').strip()
        except Exception as e: #if user manages to cause an error with their input
            print('You have entered an response that caused a ', type(e),' error.')
            print('CD Title = NA')
            cd_title = 'NA'
        try:
            cd_artist = input('What is the Artist\'s name? ').strip()
        except Exception as e: #if user manages to cause an error with their input
            print('You have entered an response that caused a ', type(e),' error.')
            print('CD Artist = NA')
            cd_artist = 'NA'
        return(cd_title, cd_artist)


# 0 general blanket try/except block around main script to catch anything I missed
try:
# 1. When program starts, read in the currently saved inventory, print program header
    lstTbl = FileProcessor.read_file(strFileName)
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    print('The Magic CD Inventory'.center(62))
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# 2. start main loop
    while True:
        # 2.1 Display Menu to user and get choice
        IO.print_menu()
        strChoice = IO.menu_choice()
        # 3. Process menu selection
        # 3.1 process exit first
        if strChoice == 'x':
            break
        # 3.2 process load inventory
        if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory will be reloaded from file.')
            try:
                strYesNo = input('Type \'yes\' to continue and reload from file - otherwise reload will be cancelled. ')
                strYesNo.lower() #testing to see if lower() causes an error
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
                continue #returns user to Main Menu
            else:
                if strYesNo.lower() == 'yes':
                    print('Reloading...')
                    lstTbl = FileProcessor.read_file(strFileName)
                    print('Inventory Loaded.')
                else:
                    print('Cancelling... Inventory data NOT reloaded.')
                IO.show_inventory(lstTbl)
            try: input('Press [ENTER] to return to Main Menu. ')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
            finally: continue  # start loop back at top.
        # 3.3 process add a CD
        elif strChoice == 'a':
            # 3.3.1 Generate ID and Ask user for CD Title and Artist
            intID = DataProcessor.calculate_cd_id(lstTbl)
            strTitle, strArtist = IO.get_cd_data()
            # 3.3.2 Add item to the table
            dicRow = DataProcessor.process_cd_data(intID, strTitle, strArtist)
            lstTbl.append(dicRow)
            IO.show_inventory(lstTbl)
            try: input('CD Added. Press [ENTER] to return to Main Menu. ')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
            finally: continue  # start loop back at top.
        # 3.4 process display current inventory
        elif strChoice == 'i':
            IO.show_inventory(lstTbl)
            try: input('Press [ENTER] to return to Main Menu. ')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
            finally: continue  # start loop back at top.
        # 3.5 process delete a CD
        elif strChoice == 'd':
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
            # 3.5.1.2 ask user which ID to remove
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
            except ValueError: #if user enters a non-integer
                print('This is not an integer.')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error.')
            # 3.5.2 search thru table and delete CD
            else:
                intRowNr, blnCDRemoved = DataProcessor.process_delete(intIDDel, lstTbl)
                if blnCDRemoved:
                    del lstTbl[intRowNr]
                    print('CD #' + str(intIDDel) + ' deleted.')
                else:
                    print('CD #' + str(intIDDel) + ' not found.')
                IO.show_inventory(lstTbl)
            try: input('Press [ENTER] to return to Main Menu. ')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
            finally: continue  # start loop back at top.
        # 3.6 process save inventory to file
        elif strChoice == 's':
            # 3.6.1 Display current inventory and ask user for confirmation to save
            IO.show_inventory(lstTbl)
            try:
                strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
                if strYesNo == 'y':
                    # 3.6.2.1 save data
                    FileProcessor.write_file(strFileName, lstTbl)
                    input('The inventory was saved to file. Press [Enter] to return to Main Menu.')
                else:
                    input('The inventory was NOT saved to file. Press [Enter] to return to Main Menu.')
            except Exception as e: #if user manages to cause an error with their input
                print('You have entered an response that caused a ', type(e),' error. Returning to Main Menu.')
            finally: 
                continue  # start loop back at top.
        # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
        else:
            print('General Error')
except Exception as e: #if user manages to cause an error with their input
    print('You have entered an response that caused a ', type(e),' error')




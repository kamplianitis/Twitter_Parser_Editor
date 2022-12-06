#####################LIBRARIES###################################
from datetime import datetime #create tweet -> for date, time 
import sys # sys.exit, exceptions
import os # io, exceptions
import json # decode binary file to ascii
import logging
import logging.config
from bisect import bisect # checks in a list where a number should be put. e.g. list=[1,5,10,58] test=6 return 2s

###################TESTING########################################
from unittest import TestCase
from unittest import mock
from nose.tools import *

'''
Enable logging according to the logger configuration file
'''
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

class TestParserEditor(TestCase):

  def resetGlobals(self):
    changesList.clear()
    globals()['change_lines'] = file_lines
    deletion_numbers_list.clear()
    globals()['deletions'] =0

  def test_createTweet(self):
    print("CreateTweet Test:")
    tweet_text = "Test Create"
    date = datetime.now()
    test_lines = change_lines
    expected_changes_list = [change_lines+1, "create", {"text": tweet_text, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text
    createTweet()
    self.assertListEqual([expected_changes_list], changesList,msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines,test_lines+1 , msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines+1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_deleteTweet_from_changesList(self):
    print("Delete List From Changes_List Test:")
    tweet_text = "Test Create"
    test_lines = change_lines
    expected_changes_list = [change_lines, "delete"]
    deleteTweet(curr_tweet_id)
    self.assertListEqual([expected_changes_list], changesList, msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines, test_lines - 1, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines - 1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")
    self.assertEqual(deletions, 1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK Deletions: PASS")

  def test_deleteTweet_from_file_no_list(self):
    print("\nDeleteTweet Test:")
    tweet_text = "Test Delete"
    changesList.clear()
    globals()['changes_lines'] = file_lines
    test_lines = change_lines
    expected_changes_list = [1, "delete"]
    deleteTweet(1)
    self.assertListEqual([expected_changes_list], changesList, msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines, test_lines -1, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, 1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_update_in_empty_changes_list(self):
    print("\nUpdateTweet Test Empty changes_list:")
    self.resetGlobals()
    test_lines = change_lines
    tweet_text = "Test Update"
    date = datetime.now()
    expected_changes_list = [56, "update",{"text": tweet_text, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text
    updateTweet(56)
    self.assertListEqual([expected_changes_list], changesList, msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines, test_lines, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, 56, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_update_in_full_changes_list(self):
    print("\nUpdateTweet Test With Full changes_list:")
    self.resetGlobals()
    tweet_text = "Test Create"
    date = datetime.now()
    test_lines = change_lines
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text
    createTweet()
    tweet_text2 = "Tweet Update"
    expected_changes_list = [[test_lines + 1, "create", {"text": tweet_text, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}],[56, "update",{"text": tweet_text2, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]]
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text2
    updateTweet(56)
    self.assertListEqual(expected_changes_list, changesList, msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines, test_lines+1, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, 56, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_update_changes_list(self):
    print("\nUpdateTweet Test With Full changes_list:")
    self.resetGlobals()
    tweet_text = "Test Create"
    date = datetime.now()
    test_lines = change_lines
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text
    createTweet()
    tweet_text2 = "Tweet Update"
    expected_changes_list = [
      [test_lines + 1, "update", {"text": tweet_text2, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]]
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text2
    updateTweet(test_lines+1)
    self.assertListEqual(expected_changes_list, changesList, msg="\tCHECK TWEET CHANGESLIST: FAIL")
    print("\tCHECK TWEET CHANGESLIST: PASS")
    self.assertEqual(change_lines, test_lines + 1, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines+1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_print_curr_tweet_id(self):
    print("\nPrint current tweet directory")
    self.resetGlobals()
    tweet_text = "Test Create"
    test_lines = change_lines
    original_input = mock.builtins.input
    mock.builtins.input = lambda _: tweet_text
    createTweet()
    self.assertEqual(change_lines, test_lines + 1, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines + 1, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")


  def test_read_last_no_deletion_no_changelist(self):
    print("\nRead last tweet no deletion no change list")
    self.resetGlobals()
    test_lines = change_lines
    readLastTweet(JsonFile)
    self.assertEqual(change_lines, test_lines, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")

  def test_read_last_deletion(self):
    print("\nRead last tweet with deletion")
    self.resetGlobals()
    test_lines = change_lines
    test_id = curr_tweet_id
    deleteTweet(test_id)
    deleteTweet(test_id-1)
    readLastTweet(JsonFile)
    self.assertEqual(change_lines, test_lines-2, msg="\tCHECK FILE LINES: FAIL")
    print("\tCHECK FILE LINES: PASS")
    self.assertEqual(curr_tweet_id, test_lines-2, msg="\tCHECK CURRENT TWEET ID: FAIL")
    print("\tCHECK CURRENT TWEET ID: PASS")


if __name__ == '__main__':
    unittest.main()


#####################GLOBAL VARIABLES#############################
# changes List.. this will be list in order to not be immutable
'''
  global variables declaration
'''
changesList = [] #list that keeps the changes done to the file
change_lines = 0 #keeps the number of lines afte the changes 
curr_tweet_id = 0 #current tweet id 
deletions = 0 # number of deletions made
deletion_numbers_list=[] # keeps the number of lines that are going to be deleted
file_lines =0 # initial lines of the file

######################FUNCTION PART#############################
# changes List.. this will be list in order to not be immutable

'''
  file_len

  Arguments:
    Arg1: (str)filename
  Returns:
    int: number of lines in given file
  Description: 
    Count the lines of given file
'''
def file_len(f): 
    for i, _ in enumerate(f): # _ goes to last expression. practically throws the last line read all the time to parse through the file
            pass
    return i + 1


'''
  createTweet

  #TODO: update curr_tweet_id to the last one --> done
  #TODO: deletion countdown ... less disk accesses --> 
  Description:
    Function that creates a new json line with the parameters text and created_at.
    The text field is given by the user while the create_at field is auto generated by
    datetime lib. 
    In the end it updates the current tweet id to the new one.
'''
def createTweet() -> None: #testing function # testing done
    tweet_text = input("Please share your thoughts:\t")
    # need the first dict to keep track of twitter_id in the changes list and update the
    globals()['change_lines'] = change_lines + 1
    # take the date from the lib
    date = datetime.now()

    # append to the changes list.
    # format the date while putting in dictionary
    changesList.append([change_lines, "create", {"text": tweet_text, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}])

    # update curr_tweet_id to the new one
    globals()['curr_tweet_id'] = change_lines
    logger.info('SUCCESS: Created tweet')

'''
  search_in_changelist


  #TODO: read in changesList correctly --> done

  Arguements:
    Arg1: int: lines --> the lines that have to be in the file with changes

  Returns:
    correct/wrong -> Str

  Description:

    The function drives through the changes list searching for the List that has as
    assigned lined to go the change_lines one. Then returns the text from the dictionary that 
    alligns with the same field found. 
'''
def search_in_changelist(lines:int) -> str:
  for i in range(len(changesList)):
    if lines == changesList[i][0] and changesList[i][1] != 'delete':
      return str(changesList[i][2]['text'])
    elif lines == changesList[i][0] and changesList[i][1] == 'delete':
      return str(changesList[i][1])
  return None

def search_greatest_in_changelist() -> str:
  great=0
  for i in range(len(changesList)):
    line = changesList[great][0]
    if line <= changesList[i][0] and changesList[i][1] != 'delete':
      great = i
  return str(changesList[great][2]['text'])


'''
  search_for_update

  Arguments:
    Arg1: (int)line
  Returns:
    int: number in list that contains the info searched
  Description: 
    function that searches if the line that is searched is already been processed but not deleted. 
'''
def search_for_update(line:int) -> int: 
  i=0
  for i in range(len(changesList)):
    if line == changesList[i][0] and changesList[i][1] != "delete":
      return i
  return -1


'''
  deleteTweet

  Arguments:
    Arg1: (int) curr_tweet_id
  Returns:
    None
  Description:
    keeps a log of the deletion asked to be made so the deletions come right after update of the file
'''
def deleteTweet(curr_tweet_id:int)-> None:
  # check if the tweet is already
  check_alter = search_for_update(curr_tweet_id)
  if(check_alter != -1):
    #case the deletion is on something on the list
    changesList[check_alter] = [curr_tweet_id, "delete"]
  else:
    # in case it hasn't altered already
    changesList.append([curr_tweet_id, "delete"])
  
  # update the necessary variables to keep track 
  globals()['deletions'] = deletions +1
  globals()['change_lines'] = change_lines -1

  if (curr_tweet_id-1 == change_lines):
    globals()['curr_tweet_id'] = change_lines
  else:
    globals()['curr_tweet_id'] =curr_tweet_id
  # update the list of deletions in order to keep track 
  deletion_numbers_list.append(curr_tweet_id)
  logger.info('SUCCESS: Tweet deleted')


'''
  check_deletions

  Arguments:
    Arg1: (int) line
  Returns: 
    int -> position that the int would have been if there are deletions
  Description:
    The function returns the position of the deletion table that the line should be inserted. This helps
    to locate how many lines we must add to our search.
'''
def check_deletions(line: int)-> int:
  # sort the array
  deletion_numbers_list.sort()
  logger.info('SUCCESS: Deletions sorted')
  return int (bisect(deletion_numbers_list, line))


'''
  read_n_to_last_line

  Arguments:
    Arg1: filename
    Arg2: number of lines from EOF, default = 1
  Returns: 
    int -> EOF
  Description:
    Reads the line that exists n number of lines from EOF. Defaults to 1, since defaulting to 0
    would end up with returning the EOF character itself.
'''
def read_n_to_last_line(filename, n = 1) -> str:
  num_newlines = 0
  try:
    filename.seek(-2, os.SEEK_END)    
    while num_newlines < n:
      filename.seek(-2, os.SEEK_CUR)
      if filename.read(1) == b'\n':
        num_newlines += 1
    last_line = str(filename.readline().decode())
    result = json.loads(str(last_line))
    logger.info('SUCCESS: Read n lines from EOF')
    return result['text']
  except OSError:
    logger.exception('FAILED: Seeking EOF')
    filename.seek(0)
    return None

'''
  updateTweet
  
  #TODO: double update search the list --> needs to be tested
'''
def updateTweet(line: int) -> None: 
  tweet_text = input("Please share your thoughts")
  date = datetime.now() 

  #check if exists already
  check_str = search_for_update(line)
  if check_str == -1:
  # append to the changes list. 
  # format the date while putting in dictionary
    changesList.append([line, "update",{"text":tweet_text , "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}])
  else:      
      changesList[check_str] = [line, "update" ,{"text":tweet_text , "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]
  #update curr_tweet_id to the new one
  globals()['curr_tweet_id'] = line
  logger.info('SUCCESS: Tweet updated')

'''
  readLastTweet

  #TODO: Case with no deletion and same values --> done
  #TODO: Case with deletion and same values -->
  #TODO: Case changes_lines > file_lines --> done
  #TODO: Case with change_lines < file_lines (NEEDS: deletion) --> 
  #TODO: Update curr_tweet_id --> done

  Usage: 
    The function checks first if the file_lines < change_lines. Case that is true, this means that we have updates not migrated.
    The function then checks the changesList array and finds the tweet with the biggest tweet_id and prints it. if the number is 
    the same, checks if there are any deletions. if not prints the last line of the file. else searches the tweet_id equal to file_lines
    and prints it. The fact that the user creates tweets that get appended only at the end of the file means that if change_lines > file_lines 
    only custom tweets will be found at last.
'''
def readLastTweet(JsonFile) -> None:
  if(file_lines == change_lines):
    if(deletions==0):
      try:
          JsonFile.seek(-2, os.SEEK_END)
          while JsonFile.read(1) != b'\n':
              JsonFile.seek(-2, os.SEEK_CUR)
          text = (JsonFile.readline().decode()) # take the tweet with the last tweet_id as a string

          result = json.loads(text) #convert it to json dict
          print("The text of the tweet with tweet id "+ str(change_lines) +" is: \n" +result['text']) #can only concat str not int
      except OSError: #Case we cannot seek in the file ... mainly this will throw cause of wrong opening (not in binary)
          JsonFile.seek(0)
          logger.info('FAILED: OS file exception in readLastTweet')
          print("Something went wrong")
    else:
      text = search_greatest_in_changelist()
      print("The text of the tweet with tweet id " + str(change_lines) + " is: \n" + str(text))
  elif(file_lines < change_lines):
    text = search_in_changelist(change_lines) # python doest not print callbacks
    print("The text of the tweet with tweet id "+ str(change_lines) +" is: \n" + str(text))
  elif change_lines < file_lines:
    read_tweet(JsonFile,change_lines)
  #Update curr_tweet_id. change lines will always have the right amount of lines that should be in the file
  globals()['curr_tweet_id'] = change_lines
  logger.info('SUCCESS: Read previous tweet')

'''
  help
  
  Usage:
    Used in case of help/h given as an input or if the user's input is wrong
'''
def help(): #testing function # testing done
  print()
  print("Options:")
  print("c : Create Tweet")
  print("r<number> : Read the tweet with tweet ID <number>")
  print("u<number> : Update the tweet at with tweet ID <number>")
  print("d : delete current tweet")
  print("$ : Read the last tweet in files")
  print("- : Read one tweet up from the current tweet ")
  print("+ : Read one tweet down from current tweet")
  print("= : Print current tweet ID")
  print("q : Quit without save")
  print("w : (Over)write file to disk")
  print("x : Exit and save")
  logger.info('SUCCESS: Displayed help message')

'''
  #TODO: Test this function
  read_tweet

  Arguments:
    Arg1: filename
    Arg2: int, current tweet id
    Arg3: int, mode, default = 0
  Returns: 
    returns -> None
  Description:
    Reads the tweet with the provided tweet_id value. Mode can be -1, 0, 1, which represents the upper adjacent 
    tweet, current tweet, and lower adjacent tweet. This value is passed by other system functions and not the user.
'''
def read_tweet(filename,curr_tweet_id: int,mode: int = 0) -> None:
  if curr_tweet_id + mode < change_lines:
    deletion_position = check_deletions(curr_tweet_id + mode)
    if deletion_position == 0:
      tweet_text = search_in_changelist(curr_tweet_id + mode)
      if tweet_text is None:
        search_line = file_lines - (curr_tweet_id + mode) + mode #find the corresponding line from the end
        print(read_n_to_last_line(filename, search_line))
      else:
        print("The text of the tweet with tweet id "+ str(curr_tweet_id+1) +" is: \n" + tweet_text)
    else:
      tweet_text = search_in_changelist(curr_tweet_id + mode + deletion_position)
      if tweet_text is None:
        search_line = file_lines - (curr_tweet_id + mode) + mode #find the corresponding line from the end
        print(read_n_to_last_line(filename, search_line))
      else:
        print("The text of the tweet with tweet id "+ str(curr_tweet_id + mode) +" is: \n" + tweet_text)
    globals()['curr_tweet_id'] = curr_tweet_id + mode
  else: # we are at the end of the file
    print("There are no more lines")
  logger.info('SUCCESS: Read current tweet')

def updateFile(file)-> None:
  #close the file
  file.close()
  #open the file
  readFile = open("testfile.json", "r")
  writeFile = open("testfile1.json", "w")
  cur_line=0
  lines_checked =0
  while cur_line < change_lines:
    if cur_line == changesList[lines_checked][0]:
      if changesList[lines_checked][1] != 'deleted':
        writeFile.write(str(changesList[lines_checked][2]) + "\n")
      if cur_line < file_lines:
        readFile.readline() # so the line checker is correct
      lines_checked = lines_checked +1 # update the lines checked already
    else:
      readLine = readFile.readline()
      writeFile.write(readLine)
  #update the values
  changesList.clear()
  deletion_numbers_list.clear()
  globals['file_lines'] = change_lines
  globals['deletions'] = 0
  logger.info('SUCCESS: Updated file')
  #remove the readed file
  os.remove('testfile.json')
  #update the name of the new one
  os.rename('testfile1.json', 'testfile.json')

'''
  checkAndExecute

  #TODO: Check for correct. --> done
  #TODO: Check max args based on file. --> abort 
  #TODO: Recommendation about the error based on command. --> done
  
  Arguments:
    Arg1 : (str) option
  Returns:
    bool : True/False 
  
  Usage: 
    Checks if the given input is valid. 

    If the input is valid the function returns True meaning the input is
    justifiable for processing. 

    If the input is not valid the function returns False meaning that input has 
    to be given again
'''
def checkAndExecute(option:str) -> None: 
  if len(option) == 1: 
    if option == 'C' or option == 'c': # testing scenario # testing done
      logger.info('Called "CREATE" process')
      createTweet()
    elif option == 'd' or option == 'D':
      logger.info('Called "DELETE" process')
      deleteTweet(curr_tweet_id)
    elif option == '$':
      logger.info('Called "READ_LAST" process')
      readLastTweet(JsonFile)
    elif option == '-':
      logger.info('Called "READ_PREVIOUS" process')
      read_tweet(JsonFile, int(curr_tweet_id), int(-1))
    elif option == '+':
      logger.info('Called "READ_NEXT" process')
      read_tweet(JsonFile, int(curr_tweet_id), int(1))
    elif option == '=': # testing scenario # testing done
      logger.info('Called "PRINT_CURRENT_ID" process')
      print(curr_tweet_id)
    elif option == 'q' or option == 'Q': # testing scenario # testing done
      logger.info('Called "Q" function')
      sys.exit("\nExiting program")
    elif option == 'w' or option == 'W':
      logger.info('Called "WRITE" process')
      updateFile(JsonFile)
    elif option == 'x' or option == 'X':
      logger.info('Called "x" function')
      updateFile(JsonFile)
      sys.exit("\nExiting program")
    elif option =='h':  #testing scenario # testing done
      logger.info('Called for help')
      help()
    else: # testing scenario #testing done
      logger.info('Wrong argument input')
      print("\nError: Wrong given argument")
      help()
  elif len(option) > 1:
    if option[0] == 'r':
      logger.info('Called "READ_TWEET" function')
      print(option)
      optionT = option.split('r', 1)
      try:
        read_tweet(JsonFile, int(optionT[1]) + 1, int(0))
      except: # testing scenario # testing done
        logger.exception('Invalid argument for "READ_TWEET" input')
        print("\nThe given argument does not translate to integer")
        help()
    elif option[0] == 'u':
      logger.info('Called "UPDATE_TWEET" function')
      optionT = option.split('u')
      try:
        updateTweet(int(optionT[1]))
      except: # testing scenario # testing done
        logger.exception('Invalid argument for "UPDATE_TWEET" input')
        print("\nThe given argument does not translate to integer")
        help()
    elif option == "help": # testing scenario # testing done
      help()
    else:  # testing scenario # testing done
      print("\nError: Wrong given argument")
      help()

def execution():
  ######################EXECUTION PART######################
  print("Twitter Editor and Viewer")


  # The following code runs as a do while
  choice = input("Give your choice:\t")
  # checkAndExecute(choice)

  while True:
    checkAndExecute(choice)
    choice = input("Give your choice:\t")

### File opening.
try:
  # open as binary helps with SEEK etc.
  JsonFile = open("testfile.json", "rb")
  print("Please wait while the file is opening")
  file_lines = file_len(JsonFile)
  change_lines = file_lines
  logger.info('SUCCESS: File opened')
except OSError:
  logger.exception('FAILED: OS file exception')
  sys.exit("File opening failed. The program will now terminate")

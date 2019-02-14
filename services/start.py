import os
import shutil
import subprocess

###------------------------------------------------------------------------------
###                               Useful variables
###------------------------------------------------------------------------------

# Needed directories
mainDir = 'services/'
mApplication = 'app/'
mStatisticsService = 'statistics_service/'
mDashboardService = 'dashboard_service/'
mCommandsService = 'dashboard_service/'
directories = [mainDir, mApplication, mStatisticsService, mDashboardService, mCommandsService]

# Files
compileScript = 'CompileScript.py'

###------------------------------------------------------------------------------
###                               Script functions
###------------------------------------------------------------------------------

## Execute a command
## Param: [command:str] the command to execute
def executeCommand(command):
    print('Executing command \'' + command + '\' ...')
    subprocess.call(command, shell=True)
    print('\'' + command + '\' successfully executed!\n')

###------------------------------------------------------------------------------
###                             Useful functions
###------------------------------------------------------------------------------

## Change directory
## Param: [path:str] the path to the target directory
def changeDirectory(path):
    print('Entering directory ' + path + ' ...\n')
    os.chdir(path)

###------------------------------------------------------------------------------
###                             Script code
###------------------------------------------------------------------------------

changeDirectory(mApplication)
executeCommand('python3 ' + 'app.py')
changeDirectory('..')
changeDirectory(mStatisticsService)
executeCommand('python3 ' + 'statistics_service.py')
changeDirectory('..')
changeDirectory(mDashboardService)
executeCommand('python3 ' + 'dashboard_service.py')
changeDirectory('..')
changeDirectory(mCommandsService)
executeCommand('python3 ' + 'commands_service.py')

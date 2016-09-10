'''
The following is an example of a decent UI with some simple functionality

@Author: David Major - Instructor
@Project: Class - Script Programming: CCM391A
@Company: Art Institute of Vancouver

Latest update: 2016/07/31 (YYYY/MM/DD)
    - All from scratch : based on work done in class and using better PyMEL examples
'''
import pymel.core as pm
win_name = 'exampleUI' # Must be a 'legal' name to Maya (A-Z, 0-9, _) !!! No spaces !!!
window_development = True # A trigger for deleting existing UI window preferences: True / False

# Set up functions: UI first, related functions next.
## UI FUNCTION ##
def UI():
    # Clean up old windows which share the name
    if pm.window(win_name, exists=True):
        pm.deleteUI(win_name)
    
    # Clean up existing window preferences
    try:
        if pm.windowPref(win_name, query=True, exists=True) and window_development:
            pm.windowPref(win_name, remove=True)
    except RuntimeError:
        pass
    
    # Declare the GUI window which we want to work with
    my_win = pm.window( win_name, widthHeight=[200,150] )
    base = pm.verticalLayout()
    
    with base: # Using the variable created 2 lines above, we can nest inside that layout element
        with pm.verticalLayout() as header: # We can also assign a variable while creating the layout element
            pm.text('Some title')
            pm.separator()
        with pm.verticalLayout(): # The assignment of a variable to the layout is optional
            #pm.button( ) # This button does nothing!
            pm.button( label='Function A', command= 'function_A()' ) # First way to execute a command with a button
        with pm.horizontalLayout() as utility:
            pm.button( label='Function B', command= function_B ) # Second way to execute a command with a button
            btn_ID = pm.button( label='Function C', backgroundColor=[0,1,0] )
                # If we were to assign the command and pass the btn_ID within the same line as creating
                # the btn_ID variable, the command errors out and will stop the script from executing
                # rather than doing it that way, we can add a command to the button after it's been created
                # and give the callback identity of the element which was created.
            btn_ID.setCommand( pm.Callback(function_C, 'test', btn_ID) ) # Third way to assign/execute a command with a button
    
    # Fix spacing of layout elements
    base.redistribute(.1)
    header.redistribute(1,.1)
    
    # Last lines of code
    my_win.show()
    #return [my_win, base, header, btn_ID] # Debugging purposes only
    

## SUPPORTING FUNCTIONS ##
def function_A(*args):
    print 'function_A activated.', args


def function_B(*args):
    print 'function_B activated.', args
    
    
def function_C(*args):
    btn_ID = args[-1]
    print btn_ID
    print 'function_C activated.', args
    btn_ID.setBackgroundColor([1,0,0])
    

# Execution of the code
UI()


## End of Code ##

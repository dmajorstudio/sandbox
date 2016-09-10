# Mockup for toolbox shell
# just messing about.

import pymel.core as pm
import os
import sys


class Toolbox(object):
    '''
    A toolbox for collecting various simple tools and scripts which are 
    able to execute independantly.
    
    Primary Use: Code examples for education and job hunting
    '''
    
    def __init__(self):
        self.verbose = True
        self.win_name = 'toolbox_ui'
        self.toolbox_path = 'C:/Users/Xanguan/Desktop/Coding/GitHub/sandbox/development/maya/python/toolbox/tool_repository'
        self.toolbox_archive = None
    
    def UI(self):
        ui_development = True
        
        # Clean up old windows which share the name
        if pm.window(self.win_name, exists=True):
            pm.deleteUI(self.win_name)
        
        # Clean up existing window preferences
        try:
            if pm.windowPref(self.win_name, query=True, exists=True) and ui_development:
                pm.windowPref(self.win_name, remove=True)
        except RuntimeError:
            pass
        
        # Declare the GUI window which we want to work with
        self.toolbox_ui = pm.window( self.win_name, 
                            title='Toolbox UI',
                            widthHeight=[200,440] )
        
        with pm.verticalLayout() as base:
            with pm.verticalLayout() as self.header:
                pm.text('Source Path', font='boldLabelFont')
            pm.separator(height=1)
            with pm.verticalLayout():
                with pm.horizontalLayout() as path:
                    self.ui_path = pm.textField(placeholderText = self.toolbox_path)
                    pm.button(label='Browse', command= self.ui_set_path)
                pm.button(label='Reload Toolbox', command= self.ui_reload_tools)
            pm.separator()
            with pm.verticalLayout() as tool_header:
                pm.text('Tools List', font='boldLabelFont')
                pm.separator()
            with pm.columnLayout(adjustableColumn=True) as self.ui_toolbox_layout:
                # Placeholder for adding new tools.
                pass
        
        # Fix spacing of layout elements
        base.redistribute(.01,.01,.15,.01,.01)
        tool_header.redistribute(.01,.01)
        
        # Last lines of code
        self.toolbox_ui.show()
        self.ui_reload_tools()
    
    
    # UI functions
    def ui_set_path(self, *uiargs, **kwargs):
        '''
        Find/set a new path for sourcing tools from
        '''
        if self.verbose: print '\t...Browsing for new path'
                
        new_path = pm.fileDialog2(fileMode=2)
        self.ui_path.setText(new_path[0])
    
    
    def ui_reload_tools(self, *uiargs, **kwargs):
        '''
        Source toolbox base path for tools scripts/folders
        '''
        if self.verbose: print '\t...Reloading tools'

        # TO-DO:
        #     Add additional registration for tools which
        #     will provide more information to the UI.
        #         - Help Info (button)
        #         - Neat name for button
        #         : This will likely require a secondary
        #         utility script to perform file parsing
        #         possibly using the ast module for literal_eval
        #         or using a JSON/XML format.
        #     - Folder support
            
        ## SIMPLE VERSION ##
        # As the simple version, only take script files at face value and execute.
        # Check paths
        if self.ui_path.getText():
            source_path = self.ui_path.getText()
        else:
            source_path = self.ui_path.getPlaceholderText()
        
        source_path = os.path.normpath(source_path)
        
        if not os.path.exists(source_path):
            pm.warning('The toolbox path you are trying to source does not exist.')
            return
        
        # Add to sys.path
        if source_path not in sys.path:
            if self.verbose: print 'Adding source path to the sys.path...'
            sys.path.append(source_path)
        
        if self.verbose: print 'Sourcing from: ', source_path
        
        # Find contents of folder and identify scripts.
        tool_dir = os.walk(source_path)
        tool_file_list = [x for x in tool_dir.next()[2] if not '__init__' in x]
        if self.verbose: print 'tool_file_list: ', tool_file_list
        
        if not tool_file_list:
            pm.warning('Could not find any valid tool files to add.')
            return
        
        # Kill old toolbox lists (archives)
        if self.toolbox_archive:
            pm.deleteUI(self.toolbox_archive)
        
        # Add UI elements which represent the files on disk.
        pm.setParent(self.ui_toolbox_layout)
        with pm.scrollLayout() as self.toolbox_archive:
            for tool in tool_file_list:                
                exec_path = os.path.join(source_path, tool)
                
                if self.verbose: print exec_path
                pm.button( label= tool.partition('.')[0], 
                           command= pm.Callback(execfile, exec_path) )



if __name__ == '__main__':
    new_box = Toolbox()
    new_box.UI()
    
    
    
    
    
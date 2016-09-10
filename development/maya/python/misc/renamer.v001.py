import pymel.core as pm

class renamer_UI():
    def __init__(self):
        self.window_name = 'DM_renamer'
    
    
    ## UI SETUP ##
    def UI(self):
        if pm.window(self.window_name, query=True, exists=True):
            pm.deleteUI(self.window_name)
        
        if pm.windowPref(self.window_name, query=True, exists=True):
            pm.windowPref(self.window_name, remove=True)
        
        with pm.window(self.window_name, width=250, menuBar=True) as my_window:
            pm.menu( label='Hints', tearOff=True )
            rename_hint = pm.menuItem( 'Rename', subMenu=True )
            pm.menuItem( 'Place consecutive #\'s for numerical incrementation.' )
            pm.menuItem( 'Use numpad enter to apply without clicking the button.' )
            
            with pm.columnLayout( adjustableColumn=True ):
                with pm.frameLayout( label='Rename', collapsable=True ):
                    pm.text('This will rename selected items from your scene.')
                    self.rename_field = pm.textField( enterCommand=self.rename_button )
                
                    with pm.frameLayout( label='Options', collapsable=True ):
                        with pm.columnLayout( adjustableColumn=True ):
                            with pm.rowLayout( numberOfColumns=4 ):
                                pm.text('Operation:', align='left')
                                self.operation_select = pm.radioCollection()
                                pm.radioButton('Rename', select=True)
                                pm.radioButton('Prefix')
                                pm.radioButton('Suffix')
                            
                            with pm.rowLayout( numberOfColumns=3 ):
                                pm.text('Hieararchy:', align='left')
                                self.hieararchy_select = pm.radioCollection()
                                pm.radioButton('Normal', select=True)
                                pm.radioButton('Chain')
                    
                    pm.button('RENAME IT!', command=self.rename_button)
                
        my_window.show()
    
    
    ## UI FUNCTIONS ##
    def rename_button(self, *args):
        self.operation_option = pm.radioCollection( self.operation_select, query=True, select=True )
        self.hieararchy_option = pm.radioCollection( self.hieararchy_select, query=True, select=True )
        
        self._rename()
    
    
    ## FUNCTIONS ##
    def _rename(self):
        node_list = pm.ls(sl=True, type='transform')
        
        if not node_list:
            raise RuntimeError('Select a root node to rename.')
        
        self.rename_name = pm.textField(self.rename_field, query=True, text=True)
        print 'Stored:', self.rename_name
        
        if not self.rename_name:
            raise RuntimeError('No valid name was input.')
        
        # Find out how many '#' characters are in the passed in name.
        digit_count = self.rename_name.count('#')
        if digit_count == 0:
            pm.warning('Name has no # sequence. Executing default renamer.')
            
            for node in node_list:
                if self.operation_option == 'Rename':
                    node.rename( self.rename_name )
                elif self.operation_option == 'Prefix':
                    node.rename( self.rename_name + node.name().rpartition('|')[2] )
                elif self.operation_option == 'Suffix':
                    node.rename( node.name().rpartition('|')[2] + self.rename_name )
            return
    
        # We need to verify that all the '#' characters are in one sequence.
        substring = '#' * digit_count     # '#' * 3 is the same as '###'
        newsubstring = '0' * digit_count  # '0' * 3 is the same as '000'
    
        # The replace command of a string will replace all occurances of the first
        # argument with the second argument.  If the first argument is not found in 
        # the string, the original string is returned.
        consecutive_check = self.rename_name.replace(substring, newsubstring)
        
        if consecutive_check == self.rename_name:
            raise RuntimeError('Pound signs must be consecutive..')
        
        # Setup the replacement string to be used in the looping section.
        self.rename_name = self.rename_name.replace(substring, '%0{0}d'.format(digit_count))
        
        self.numerical_iter = 1
        for node in node_list:
            self._rename_numerical(node=node)
        
    
    def _rename_numerical(self, node, *args):
        new_name = (self.rename_name % self.numerical_iter)
                
        if self.operation_option == 'Rename':
            node.rename( new_name )
        elif self.operation_option == 'Prefix':
            node.rename( new_name + node.name().rpartition('|')[2] )
        elif self.operation_option == 'Suffix':
            node.rename( node.name().rpartition('|')[2] + new_name )
        
        self.numerical_iter += 1
        
        if self.hieararchy_option == 'Chain':
            child_list = pm.listRelatives(node, children=True, type='transform') or []
            
            for child in child_list:
                self._rename_numerical(node=child)


myUI = renamer_UI()
myUI.UI()

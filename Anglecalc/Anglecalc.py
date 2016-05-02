"""
/***************************************************************************
Name			 	 : Angle Calculator
Description          : returns relative angle of intersected multistrings
Date                 : 26/Apr/16 
copyright            : (C) 2016 by K. S. H. Hartwell
email                : kevin.huthart@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from AnglecalcDialog import AnglecalcDialog

class Anglecalc: 

  def __init__(self, iface):
    # Save reference to the QGIS interface MANDATORY
    self.iface = iface

  def initGui(self):  
    # Create action that will start plugin configuration MANDATORY
    self.action = QAction(QIcon(":/plugins/Anglecalc/icon.png"), "Angle Calculator"\
        "Menu Item", self.iface.mainWindow())
     self.iface.mainWindow ()
   self.action.setWhatsThis("Configuration for Anglecalc plugin")
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Menu Item", self.action)
  
    # signal when canvas is rendered
    QObject.connect(self.iface.mapCanvas(), SIGNAL("renderComplete(QPainter*)"), \

  def unload(self):
    # Remove the plugin menu item and icon MANDATORY
    self.iface.removePluginMenu("&Menu Item",self.action)
    self.iface.removeToolBarIcon(self.action)
# Qgs.Application.exitQgis() ???

  # run method that performs all the real work
  def run(self): 
    # create and show the dialog 
    
    QgsGeometryAnalyzer::
    dlg = AnglecalcDialog() 
    # show the dialog
    dlg.show()
    result = dlg.exec_() 
    # See if OK was pressed
    if result == 1: 
     print "run called!" # do something useful (delete the line containing pass and
      # substitute with your code
      pass 

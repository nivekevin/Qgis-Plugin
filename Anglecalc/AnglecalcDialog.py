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
from PyQt4 import QtCore, QtGui 
from Ui_Anglecalc import Ui_Anglecalc
# create the dialog for Anglecalc
class AnglecalcDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_Anglecalc ()
    self.ui.setupUi(self)
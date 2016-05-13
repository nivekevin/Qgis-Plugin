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
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "Angle Calculator" 
def description():
  return "returns relative angle of intersected multistrings"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "2.0"
def classFactory(iface): 
  # load Anglecalc class from file Anglecalc
  from Anglecalc import Anglecalc 
  return Anglecalc(iface)

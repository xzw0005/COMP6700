'''
Created on Aug 30, 2015

@author: XING WANG (xzw0005@tigermail.auburn.edu)
'''
import os
import math

class StarCatalog(object):
    '''
    StarCatalog is an abstraction that represents an inventory of stars that are visible from earth. 
    Associated with each star is its catalog identifier, the magnitude of its brightness, its right ascension, and its declination.                
    '''
    def __init__(self):
        '''
        Constructor: Creates an instance of a StarCatalog.
        '''
        self.catalog = {}

    def loadCatalog(self, starFile = None):
        """
        Loads the star catalog from a text file containing star data.
        """
        if (starFile == None or type(starFile) != str):
            raise ValueError("The file name violates the parameter specifications.")
        if (os.path.isfile(starFile)):
            f = open(starFile, 'r')
        else:
            raise ValueError("No file exists by the specified file name.")
        for line in f:
            lineList = line.split("\t")
            if (len(lineList) != 4):
                raise ValueError("A problem arises when parsing the file for star data.")
            for element in lineList:
                try:
                    float(element)
                except ValueError:
                    raise ValueError("A problem arises when parsing the file for star data.")
            #if (lineList[2] < 0) or (lineList[2] >= math.pi * 2) 
            #        or (lineList[3] < -math.pi/2) or (lineList[3] > math.pi/2):
            #    raise ValueError("A problem arises when parsing the file for star data.")
            if int(lineList[0]) in self.catalog.keys():
                raise ValueError("An attempt is made to add a duplicate star to the catalog.")
            self.catalog[int(lineList[0])] = [float(x) for x in lineList[1:]]
        f.close()
        return len(self.catalog)
    
    def emptyCatalog(self):
        """ Deletes all stars from the catalog.
            An integer count of the number of stars deleted from the catalog.
        """
        count = len(self.catalog)
        self.catalog = {}
        return count

    def getStarCount(self, lowerMagnitude = None, upperMagnitude = None):
        """ Returns the number of stars in the star catalog that 
            have a magnitude within the range [lowerMagnitude, upperMagnitude].
        """
        if (lowerMagnitude == None):
            lowerMagnitude = min(val[0] for val in self.catalog.values())
        if (upperMagnitude == None):
            upperMagnitude = max(val[0] for val in self.catalog.values())
        if (not isinstance(lowerMagnitude, (float, int, long))):
            raise ValueError("Invalid input: upperMagnitude violates its specfication.")
        if (not isinstance(upperMagnitude, (float, int, long))): #or (upperMagnitude < 0):
            raise ValueError("Invalid input: lowerMagnitude violates its specfication.")
        if (lowerMagnitude > upperMagnitude):
            raise ValueError("Invalid input: lowerMagnitude is greater than upperMagnitude!")
        count = 0
        for val in self.catalog.values():
            if (val[0] >= lowerMagnitude and val[0] <= upperMagnitude):
                count+=1
        return count
    
    
    def getMagnitude(self, rightAscensionCenterPoint=None, declinationCenterPoint=None, fieldOfView=None):
        """ Returns numeric value of the magnitude of the brightest star within the field of view; 
            returns "None" if no stars are in the field of view.
        """       
        if (rightAscensionCenterPoint==None) or (not isinstance(rightAscensionCenterPoint, (float, int, long))) or (rightAscensionCenterPoint < 0) or (rightAscensionCenterPoint > math.pi * 2):
            raise ValueError("Invalid input: rightAscensiionCenterPoint violates its specification.")
        if (declinationCenterPoint==None) or (not isinstance(declinationCenterPoint, (float, int, long))) or (declinationCenterPoint < -math.pi/2) or (declinationCenterPoint > math.pi/2):
            raise ValueError("Invalid input: declinationCenterPoint violates its specification.")
        if (fieldOfView==None) or (not isinstance(fieldOfView, (float, int, long))) or (fieldOfView < 0) or (fieldOfView > math.pi * 2):
            raise ValueError("Invalid input: fieldOfView violates its specification.")
        magnitudeInField = []
        for val in self.catalog.values():
            if (val[1] >= rightAscensionCenterPoint - fieldOfView / 2.0) and (val[1] <= rightAscensionCenterPoint + fieldOfView / 2.0):
                if (val[2] >= declinationCenterPoint - fieldOfView / 2.0) and (val[2] <= declinationCenterPoint + fieldOfView / 2.0):
                    magnitudeInField.append(val[0])
        if (len(magnitudeInField) == 0):
            return None
        else:
            return min(magnitudeInField)
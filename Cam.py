
from ast import Global


class Cam:
    def __ini__(self, id, enabled, description, fileLocation, restrictionTime):
        self.id = id
        self.enabled = enabled
        self.description = description
        self.fileLocation = fileLocation
        self.restrictionTime = restrictionTime
    
    def setId(self, id):
        self.id = id
    
    def setEnabled(self, enabled):
        self.enabled = enabled
    
    def setDescription(self,description):
        self.description = description
    
    def setFileLocation(self, fileLocation):
        self.fileLocation = fileLocation
    
    def setRestrictionTime(self, restrictionTime):
        self.restrictionTime = restrictionTime
        
    def getId(self):
        return self.id
    
    def getEnabled(self):
        return self.enabled
    
    def getDescription(self):
        return self.description
        
    def getFileLocation(self):
        return self.fileLocation
    
    def getRestrictionTime(self):
        return self.restrictionTime
        
    
    
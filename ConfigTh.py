#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[ ]:


class ConfigTh:
    def __init__(self, path, selection, era = "Theory"):
        self.configdir = os.getcwd()+"/../conf/config"
        
        self.projectdir = self.getProjectDir()
        self.path = path 
        self.era  = era
        self.selection = selection

        self.date = self.__setDate()
        self.figpath = self.projectdir+"figs/"+era+"/"+selection+"/"
        self.jsondir = self.projectdir+"json/"
        
        self.dirStructure()
        
    def __repr__(self):
        space = len(ConfigTh.__name__)
        spacer = " "*space
        msg = "{}(path={},\n".format(ConfigTh.__name__,self.path)
        msg += spacer+"*selection={},\n".format(self.selection)
        msg += spacer+"*era={},\n".format(self.era)
        msg += spacer+")\n"
        msg += spacer+"--> projectdir: {} (extracted from {})\n".format(self.projectdir, self.configdir)
        msg += spacer+"--> date: {}\n".format(self.date)
        msg += spacer+"--> figpath: {}\n".format(self.figpath)
        msg += spacer+"--> jsondir: {}\n".format(self.jsondir)
        
        return msg
    
    def __del__(self):
        del self.projectdir
        del self.path 
        del self.era  
        del self.selection
        del self.date
        del self.figpath 
        del self.jsondir 
        
    def __setDate(self):
        import datetime
        date = datetime.datetime.now()
        return str(date.year) + str(date.month) + str(date.day) + "/"
    
    def _setProjectDir(self, projectdir):
        self.projectdir = projectdir
    
    def _setPath(self, path):
        self.path = path
        
    def _setEra(self, era):
        self.era = era
    
    def _set(self,var,value):
        setattr(self,var,value)    
        
    def getProjectDir(self):
        with open(self.configdir) as f:
            projectdir = f.read()
        return projectdir.split('\n')[0]

    def CreateDir(self,figpath,fileName='',sufix='', Print = False):
        try:
            os.mkdir(figpath+fileName+sufix) 
        except:
            if Print:
                print("Directory "+fileName+sufix+ " already exist")    
    
    def dirStructure(self,Print = False):
        path = self.figpath + self.date
        
        self.CreateDir(path)
        self.dirSubStructure(path +   "Stacked/", Print=Print)
        self.dirSubStructure(path + "Unstacked/", Print=Print)


    def dirSubStructure(self, path,Print = False):
        self.CreateDir(path, Print=Print)
        self.CreateDir(path+"log",Print=Print)
        self.CreateDir(path+"log/Mult", Print=Print)
        self.CreateDir(path+"linear", Print=Print)
        self.CreateDir(path+"linear/Mult", Print=Print)


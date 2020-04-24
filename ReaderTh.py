#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd 
from root_pandas import read_root
import re


# In[1]:


class ReaderTh():
    def __init__(self, Config, Print = False):
        self.Config = Config
        
        self.projectdir = Config.projectdir
        self.path = Config.path 
        self.era  = Config.era
        self.selection  = Config.selection
        self.pathtmp = None
            
        self.Print     = Print
        
    def __del__(self):
        del self.Config
        del self.pathh
        del self.era
        del self.selection
        del self.Print
        
    def __repr__(self):
        space = len(ReaderTh.__name__)
        spacer = space*" "
        msg  = "{}(Config={},Print={})".format(ReaderTh.__name__,self.Config,self.Print) 
        msg += spacer+"--> projectdir: {}".format(self.projectdir)
        msg += spacer+"--> path: {}".format(self.path)
        msg += spacer+"--> era: {}".format(self.era)
        msg += spacer+"--> selection: {}".format(self.selection)
        return msg
    
    def __lineFormat(self, line):
        val = []
        for inline  in re.split(' +',line):
            try: val.append(float(inline))
            except: pass
        return val
    
    def read(self):
        try:
            data = self.readTheory()
        except:
            print("Failed reading file")
        return data
    
    def readTheory(self,generator,order,coupling,value,var, Print = False):
        
        if generator == "mcfm":
            path = self.path + generator+"/"+self.era+"/"+order+"/"+coupling+"/"
            path = path+value+"/" if coupling.lower() != "sm" else path
            path += self.getFileName(order,var)
            self.pathtmp = path
            try:
                bins,xsec,err,ranges = self.getXsec(generator, path, Print=Print)
            except:
                bins,xsec,err,ranges = [], [], [], []
                
        elif generator == "matrix":
            path = self.path + generator+"/"+self.era+"/"+order+"/"+coupling+"/"
            path = path+value+"/" if coupling.lower() != "sm" else path
            path += self.getFileName(order,var)
            self.pathtmp = path
            try:
                bins,xsec,err,ranges = self.getXsec(generator, path, Print=Print)
            except:
                bins,xsec,err,ranges = [], [], [], []
        else:
            bins,xsec,err,ranges = [], [], [], []
                
    
        xsecOut = {
                    "bins":bins,
                    "xsec":xsec,
                    "err":err,
                    "ranges":ranges
                    }
        
        return xsecOut
    def getFileName(self,order,var):
        if self.selection == "mcfm":
            return "Zgamma_"+order+"_MMHT_nl_1____1____14TeV_"+var+".txt"
        elif self.selection == "matrix":
            return var+"__"+order.upper()+".dat"
        else:
            return ""

    def getRanges(self,generator,filename,Print=False):
        if Print:
            print("--gen",generator)
            print("--filename",filename)
        
        ranges = None
        if generator == "mcfm":
            var = filename.split('_')[-1]
            var = var.split('.')[0]
            
            ranges = [0,100]

            if   'mass' in var: ranges = [50,200]

            elif "pt3" in var : ranges = [25,100]
            elif "pt4" in var : ranges = [20,100]
            elif "pt5" in var : ranges = [20,500]
            elif "pt6" in var : ranges = [0,500]

            elif "y3" in var : ranges = [-3,3]
            elif "y4" in var : ranges = [-3,3]
            elif "y5" in var : ranges = [-3,3]
            elif "y6" in var : ranges = [-3,3]
            elif "ydiff(Vgam)" in var  : ranges = [-5,5]
        elif generator == "matrix":
            filename = filename.split('/')[-1]
            #var = ""
            #var.join(filename.split('_')[:-1])
            var = filename.split('_')[0]
            
            if Print:
                print("--gen",generator)
                print("--filename",filename)
                print("--var",var)
        
            
            if    "mlep1lep2" in var: ranges = [50,200]
            elif  "mlep1lep2gamma" in var: ranges = [0,500]
                
            elif "pTlep1lep2" in var: ranges = [20,500] 
            elif "pTlep1" in var: ranges = [20,100] 
            elif "pTlep2" in var: ranges = [20,100]
            elif "pTgamma" in var: ranges = [20,500]
            
            elif "dRlep1gamma" in var : ranges = [-3,3]
            elif "dRem1ep1" in var : ranges = [-3,3]
            
            elif 'pT' in var: ranges = [0,500]
            elif 'm' in var: ranges = [0,500]
            elif 'dR' in var: ranges = [-3,3]
                
        if Print:
            print(var)
                
        return ranges
    
    def getXsec(self,generator, filename, Print=False):
        bins = []
        xsec = []
        xsecerr = []
        with open(filename,'r') as file:
                for line in file:
                    if '#' not in line:
                        values = self.__lineFormat(line)
                        
                        if generator == "mcfm":  
                            bins.append(values[:2])
                            xsec.append(values[2])
                            xsecerr.append(values[3])

                            ranges = self.getRanges(generator,filename,Print=Print)
                        elif generator == "matrix":
                            bins.append(values[0])
                            xsec.append(values[1])
                            xsecerr.append([values[3], values[5]])
                            
                            ranges = self.getRanges(generator,filename,Print=Print)
            
        return bins,xsec,xsecerr,ranges
        


# In[ ]:





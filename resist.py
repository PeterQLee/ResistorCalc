from copy import copy
class Resist:
    def __init__(self,optw):
        """
        Initialize the function with either a dictionary of resistors, list, or a string (csv), or a file pointer"""
        self.rescount=[]
        self.resdict={}
        self.resval=[]
        self.seriesdict={}
        self.masterlist=[]
        self.mastervals=[]
        self.listlen=0
        if type(optw) is dict:
            pass
        if type(optw) is list:
            #if no units specified, assume ohms
            
            for i in optw:
                j=self.convertOhm(i)
                if j in self.resdict:
                    self.resdict[j]+=1
                    rescount[rescount.index(j)]+=1
                    #increment rescount
                else:
                    self.resdict[j]=1
                    self.rescount.append(1)
                    self.resval.append(j)
            self.listlen=len(self.masterlist)
        if type(optw) is str:
            pass
        # if type(optw) is file:
        #     #guess format
        #     #1get data and input
        #     1g=optw.read()
        #     #parse and stuff
        else :
            pass #tell user unaccepted type
        self.compileAdds(0,0,[0]*len(self.resval))
        
        
    def convertOhm(self,val):
        return int(val) #converts ohm
    def compileAdds(self,ind,curval,usedindices): #calculates all the series
        if ind<len(self.rescount):
            for i in range(1,self.rescount[ind]+1):
                addval=curval+self.resval[ind]*i #get new resistor value
                g=copy(usedindices) #[0,0,1,0,0,...]
                g[ind]+=i
                #add to master list
                self.masterlist.append(g)
                self.mastervals.append(addval)
                self.listlen+=1
                self.compileAdds(ind+1,addval,g)
            self.compileAdds(ind+1,curval,usedindices)
    def approxResistor(self,desiredohm,depth=-1):
         #depth flag is for specify amount of recursion depth
         #this will use series / parallels in order to attempt to get the closest value of var_desiredohm as possible
         #right now using a simple graph search algorithm, hopefully i can beef it up a bit later.
         #NOTE TO SELF, ENSURE THAT EVERYTHING IS SORTED BY HIGHEST TOTAL RESISTANCE. (highest to lowest)
         
        #resultlist=[[self.mastervals[0],self.masterlist[0]]]
         #resultlist takes form of value, then the list of resister ID's
        result=([],[])
        for i in range(1,len(self.masterlist)):
             tmp=self.recursefunc(self.mastervals[i],self.masterlist[i],[i],[])
             result=(result[0]+tmp[0],result[1]+tmp[1])
        return result
    def getAvailableRes(self,usedres):
        #gets possible resistor groups(ids) which can be combined with current setup.
        result=[]
        for i in range(self.listlen):
            print (i,usedres,self.masterlist[i],self.rescount)
            g=map(self.subtract,usedres,self.masterlist[i],self.rescount) #we need some kind of ordering to optimize this
            if False in g:
                pass
            else:
                result.append(i)
        return result
        
    def subtract(self,a,b,c):
        return (c-a-b)>=0
    
    def computeSeries(self,ohm1,ohm2):
        print(ohm1,ohm2)
        return ohm1+ohm2
    
    def computeParallel(self,ohm1,ohm2):
        return 1/(1/ohm1+1/ohm2)
    
    def recursefunc(self,currentohmval,usedres,idlist,operation): #rename this
        #this function computes ALL posibilities, it is really bad, but alas a start
        #operation: 0:series, 1:parallel
        
        possiblechoose=self.getAvailableRes(usedres)

        #no possibilities, just return
        if len(possiblechoose)==0: return ([idlist],[operation]) #find a better way to do this
        ret=([],[])
        
        for i in possiblechoose:
            newusedres=[x+y for x,y in zip(usedres,self.masterlist[i])]
            newidlist=idlist+[i]
            tmp=self.recursefunc(self.computeSeries(currentohmval,self.mastervals[i]),newusedres,newidlist,operation+[0])
            ret=(ret[0]+tmp[0],ret[1]+tmp[1])
            print("ayy",ret)
            tmp=self.recursefunc(self.computeParallel(currentohmval,self.mastervals[i]),newusedres,newidlist,operation+[1])
            ret=(ret[0]+tmp[0],ret[1]+tmp[1])

        return ret
            

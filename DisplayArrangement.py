from tkinter import *
class ResistorGroup:#various inheritance
    #instead of canvas, we may have to use 
    def __init__(self,colors):
        self.height=2
        self.width=1
        #self.create_rectangle(etcEtc)
        #rect dims (0.5x1)
        self.spacinghor=0.5
        self.rectcoords=[0,0.5]
        self.linecoords=[0.25,0.0,0.25,0.5,0.25,1.5,0.25,2.0]#maybe make line len 0.5, so adds up to 1
        self.values=[colors]
    def addSeries(self,other):
        #add height and width
        #

        #optionally, insert resistor value for user reference!!@!@!!
        self.values+=other.values
        
        for i in range(0,len(other.rectcoords),2):
            self.rectcoords.append(other.rectcoords[i])
            self.rectcoords.append(other.rectcoords[i+1]+self.height)
        for i in range(0,len(other.linecoords),2):
            self.linecoords.append(other.linecoords[i])
            self.linecoords.append(other.linecoords[i+1]+self.height)
        #now add a line for the width difference
        # | |
        # ___
        # | |
        divider=[0.25,self.height,self.width-1+0.25,self.height]
        self.linecoords+=divider
        #the 0.25 may change based on where the series are placed
            
        self.height+=other.height#+linelen

        
        self.width=max(other.width,self.width)
        #add new canvas adding this one
        #ensure a "wire" is connecting both of them
        
        #draws a line __ above depending on width of other
    def addParallel(self,other):
        self.values+=other.values
        for i in range(0,len(other.rectcoords),2):
            self.rectcoords.append(other.rectcoords[i]+self.width)
            self.rectcoords.append(other.rectcoords[i+1])
        for i in range(0,len(other.linecoords),2):
            self.linecoords.append(other.linecoords[i]+self.width)
            self.linecoords.append(other.linecoords[i+1])

        #this divider will be complicated, will have to elongate the line of shorter length
        oldwidth=self.width
        self.width+=other.width
        divider=[0.25,0,self.width-1+0.25,0]
        oldh=self.height
        
        self.height=max(other.height,self.height)
        divider+=[0.25,self.height,self.width-1+0.25,self.height]
        #start elongated one end or other
        if self.height==other.height:
            divider+=[0.25,self.height,0.25,oldh]
        else:
            divider+=[oldwidth+0.25,self.height,oldwidth+0.25,other.height]
        self.linecoords+=divider
            
        
        
    
                        
        
    
    
class DisplayArrangement:
    colormap=['black','brown','red','orange','yellow','green','blue','violet','grey','white']
    def __init__(self):
        self.tkroot=Tk()
        self.w=200
        self.h=200
        self.canvasframe=Frame(self.tkroot,height=self.h,width=self.h,padx=5,pady=5)
        self.canvasframe.pack(side=TOP)
        w=Canvas(self.canvasframe,width=self.w,height=self.h,bd=0,highlightthickness=0)
        w.pack()
        
        self.buttonframe=Frame(self.tkroot,height=30)
        self.buttonframe.pack(side=BOTTOM)
        self.makeHUD()
        
        
        self.canvas=w
        self.canvas.create_line(0,0,0,200)
        
    def getResColor (self,resval):
        v=str(resval)
        return (self.colormap[int(v[0])],self.colormap[int(v[1])],self.colormap[len(v)-2])
    def makeHUD(self):
        #last 30 pixels of y dedicated for buttons
        self.backbutton=Button(self.buttonframe,text="Back")
        self.backbutton.pack(side=LEFT,)
        self.showbutton=Button(self.buttonframe,text="Show Ohms")
        self.showbutton.pack()
        self.nextbutton=Button(self.buttonframe,text="Next")
        self.nextbutton.pack(side=RIGHT,)
    def draw(self,vals,operations):
        #vals are the values of the resistors,
        #operations determine whether it is in series or parallel

        #first we need to get the arrangement of resistors and thus
        #draw the diagram with it

        ycols=operations.count(0)
        #the number of series in this operation

        xcols=operations.count(1)
        #parallels

        
        curmap=[[]]*ycols
        x=0
        y=0    
        for i in range(len(vals)):
            curmap[y].append(vals[i])
    def nextsymbol(self,st):
        if st[0]=='-' or st[0]=='+':
            return (st[0],st[1:len(st)])
        else:
            ind=0
            go=True
            while go:
                try:
                    int(st[ind])
                    ind+=1
                except:
                    go=False
            #get rid of comma
            return (int(st[0:ind]),st[ind+1:])

    # def drawGrid(self,grid):
    #     tmpxdiv=3
    #     tmpydiv=3
    #     width=self.w/tmpxdiv
    #     height=self.h/tmpydiv

    #     offset=10
        
    #     for x in range(tmpxdiv):
    #         for y in range(tmpydiv):
    #             if grid[y][x]!=-1:
    #                 self.canvas.create_rectangle(x*width+offset,y*height+offset,(x+1)*width-offset,(y+1)*height-offset)
                    #now make stripes for the resistor
    def drawRes(self,posx,posy,value):
        pass
    def newDraw(self,postfix):
        #resistors are stored in postfix notation
        

        #clear canvas
        self.canvas.delete('all')
        
        
        cells=[]
        canvasCells=[]
        
        
        while postfix!="":
            symbol,postfix=self.nextsymbol(postfix)
            # if symbol=='+':
            #     tmp=cells.pop()
            #     self.drawRes(basex,curycord,tmp)
            #     self.drawRes(basex,curycord+1,cells[len(cells)-1])
            #     #need a way of connecting these
            #     cells[len(cells)-1]+=tmp
            #     #add last two values

                
            #     curycord+=1
                
            #     if curycord>ycellcord:
            #         ycellcord=curycord
            if symbol=='+':
                print(len(cells)-1)
                tmp=cells.pop()
                print(len(cells)-1)                
                cells[len(cells)-1]+=tmp
                tmp=canvasCells.pop()
                canvasCells[len(canvasCells)-1].addSeries(tmp)
            elif symbol=='-':
                tmp=cells.pop()
                cells[len(cells)-1]+=tmp
                tmp=canvasCells.pop()
                canvasCells[len(canvasCells)-1].addParallel(tmp)
            # elif symbol=='-':
            #     tmp=cells.pop()
            #     self.drawRes(curxcord,curycord,tmp)
            #     self.drawRes(curxcord+1,curycord,cells[len(cells)-1])
            #     #need a way of connecting these
            #     cells[len(cells)-1]=1/cells[len(cells)-1]+1/tmp
            #     curxcord+=1
            
            else:
                cells.append(symbol)
                canvasCells.append(ResistorGroup(symbol))#self.getResColor(symbol))
        obj=canvasCells[0]
        factor=(self.h-40)/obj.height
        print(obj.rectcoords) #TMP
        print(obj.linecoords)
        for i in range(0,len(obj.rectcoords),2):
            
                #draw rectangle + appropritate color, for now we will just draw a regular rectangle
                # we will make a function for resistor drawing later
            self.canvas.create_rectangle(obj.rectcoords[i]*factor,(obj.rectcoords[i+1])*factor,(obj.rectcoords[i]+0.5)*factor,(obj.rectcoords[i+1]+1)*factor)
            #now make colored rectangles
            cols=self.getResColor(obj.values[i//2])
            self.canvas.create_rectangle(obj.rectcoords[i]*factor,obj.rectcoords[i+1]*factor,(obj.rectcoords[i]+0.5)*factor,(obj.rectcoords[i+1]+1/3)*factor,fill=cols[0])
            self.canvas.create_rectangle(obj.rectcoords[i]*factor,(obj.rectcoords[i+1]+1/3)*factor,(obj.rectcoords[i]+0.5)*factor,(obj.rectcoords[i+1]+2/3)*factor,fill=cols[1])
            self.canvas.create_rectangle(obj.rectcoords[i]*factor,(obj.rectcoords[i+1]+2/3)*factor,(obj.rectcoords[i]+0.5)*factor,(obj.rectcoords[i+1]+1)*factor,fill=cols[2])
            
            
        for i in range(0,len(obj.linecoords),4):
            self.canvas.create_line(obj.linecoords[i]*factor,obj.linecoords[i+1]*factor,obj.linecoords[i+2]*factor,obj.linecoords[i+3]*factor)
        return canvasCells
            
            

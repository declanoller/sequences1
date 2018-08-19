import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
from datetime import datetime
from math import floor,sqrt,cos,sin,pi
import numpy as np

class Sequence:

    def __init__(self,type,length,x0):
        fn_dict = {
        'tent':self.tentSeq,
        'collatz':self.collatz,
        'recaman':self.recaman,
        'georecaman':self.geoRecaman,
        'juggler':self.juggler
        }
        self.type = type
        self.length = length
        self.x0 = x0
        self.seq_func = fn_dict[self.type]

        self.recamanSeq = None

        self.fibpair = [1,1]

    def tentSeq(self,x):
        if x<.5:
            return(2*x)
        if x>=.5:
            return(2-2*x)


    def juggler(self,x):
        if x==1:
            return(1)
        if x%2==0:
            return(floor(x**0.5))
        else:
            return(floor(x**1.5))


    def collatz(self,x):
        if x==1:
            return(1)
        if x%2==0:
            return(int(x/2))
        else:
            return(3*x+1)


    def recaman(self,x):
        if self.recamanSeq==None:
            self.recamanSeq = []
            self.recamanSet = set(self.recamanSeq)

        skip = len(self.recamanSeq)+1

        if (x-skip) not in self.recamanSet and (x-skip)>0:
            self.recamanSeq.append(x-skip)
            self.recamanSet.add(x-skip)
            return(x-skip)
        else:
            self.recamanSeq.append(x+skip)
            self.recamanSet.add(x+skip)
            return(x+skip)


    def geoRecaman(self,x):
        if self.recamanSeq==None:
            self.recamanSeq = []
            self.recamanSet = set(self.recamanSeq)

        skip = len(self.recamanSeq)+1
        skip = 2**skip

        if (x-skip) not in self.recamanSet and (x-skip)>0:
            self.recamanSeq.append(x-skip)
            self.recamanSet.add(x-skip)
            return(x-skip)
        else:
            self.recamanSeq.append(x+skip)
            self.recamanSet.add(x+skip)
            return(x+skip)

    def produceSeq(self):

        self.seq = [self.x0]
        x = self.x0
        for i in range(self.length):
            x = self.seq_func(x)
            self.seq.append(x)

        print(self.seq)


    def plotSeq(self):

        plt.plot(self.seq)
        plt.show()


    def drawCircleSeq(self):

        img_size = (2*640,2*480)
        margin = 0.05*img_size[0]

        max_diff = max([abs(self.seq[i+1]-self.seq[i]) for i in range(len(self.seq)-1)])
        x_range = max(self.seq) - min(self.seq)

        color_scale = 360/max_diff

        size_dilate = min( (img_size[0] - 2*margin)/x_range, (img_size[1]-2*margin)/max_diff)

        x_margin = (img_size[0]-x_range*size_dilate)/2.0

        center_y = img_size[1]/2
        im = Image.new(mode='RGB',size=img_size,color='white')
        draw = ImageDraw.Draw(im)

        circle_width = 50
        x0 = self.seq[0]
        for i in range(len(self.seq)-1):
            pair = [self.seq[i],self.seq[i+1]]
            x1 = min(pair)
            x2 = max(pair)
            circle_width = x2 - x1
            y1 = -circle_width/2
            y2 =  circle_width/2

            angle_offset = 180*(i%2)

            x1 *= size_dilate
            x2 *= size_dilate
            y1 *= size_dilate
            y2 *= size_dilate

            x1 += x_margin
            x2 += x_margin
            y1 += center_y
            y2 += center_y

            draw.arc([x1,y1,x2,y2],angle_offset+0,angle_offset+180,fill='black')
            #draw.arc([x1,y1,x2,y2],angle_offset+0,angle_offset+180,fill='hsl({},100%,45%)'.format(int(color_scale*circle_width)))



        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = '{}_{}terms_x0={}_{}.png'.format(self.type,self.length,self.x0,date_string)
        print(fname)
        im.save(fname)

        im.show()



    def drawGradientLine(self,imdraw,coords,hue):
        #draws a gradient from black at point 1 to the hue at point 2
        sections = 40
        (x1,y1,x2,y2) = coords
        base_pt = np.array([x1,y1])
        offset = np.array([x2-x1,y2-y1])
        offset_step = offset/sections

        line_width = 6

        for i in range(sections):
            col_string = 'hsl({},100%,{}%)'.format(hue,int(50*(i/sections)))
            line_pts = np.concatenate((base_pt + i*offset_step, base_pt + (i+1)*offset_step)).tolist()
            imdraw.line(line_pts,width=line_width,fill=col_string)


        #im.show()


    def drawMiddleGradientLine(self,imdraw,coords,hue):
        (x1,y1,x2,y2) = coords
        midpoint_x = (x1 + x2)/2.0
        midpoint_y = (y1 + y2)/2.0

        line1_pts = [x1,y1,midpoint_x,midpoint_y]
        line2_pts = [x2,y2,midpoint_x,midpoint_y]

        self.drawGradientLine(imdraw,line1_pts,hue)
        self.drawGradientLine(imdraw,line2_pts,hue)

    def drawTriangleSeq(self):

        img_size = (2*640,2*480)
        margin = 0.05*img_size[0]

        max_diff = max([abs(self.seq[i+1]-self.seq[i]) for i in range(len(self.seq)-1)] + [abs(self.seq[-1]-self.seq[-2])])
        x_range = max(self.seq) - min(self.seq)
        color_scale = 360/max_diff

        size_dilate = min( (img_size[0] - 2*margin)/x_range, (img_size[1]-2*margin)/max_diff)
        x_margin = (img_size[0]-x_range*size_dilate)/2.0
        center_y = img_size[1]/2
        im = Image.new(mode='RGB',size=img_size,color='white')
        draw = ImageDraw.Draw(im)

        x0 = self.seq[0]
        min_term = min(self.seq)
        for i in range(len(self.seq)-1):
            pair = [self.seq[i],self.seq[i+1]]
            x1 = min(pair) - min_term
            x2 = max(pair) - min_term
            dist = x2 - x1
            y1 = 0
            y2 = dist/2


            x1 *= size_dilate
            x2 *= size_dilate
            y1 *= size_dilate
            y2 *= size_dilate
            y2 *= (-1)**i

            x1 += x_margin
            x2 += x_margin
            y1 += center_y
            y2 += center_y

            midpoint = (x1 + x2)/2
            #draw.line([x1,y1,midpoint,y2],width=3,fill='black')
            #draw.line([x2,y1,midpoint,y2],width=3,fill='black')
            if x1==x2:
                break
            self.drawGradientLine(draw,[x1,y1,midpoint,y2],int(color_scale*dist))
            self.drawGradientLine(draw,[x2,y1,midpoint,y2],int(color_scale*dist))
            #draw.arc([x1,y1,x2,y2],angle_offset+0,angle_offset+180,fill='hsl({},100%,45%)'.format(int(color_scale*dist)))



        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = '{}_tri_{}terms_x0={}_{}.png'.format(self.type,self.length,self.x0,date_string)
        print(fname)
        im.save(fname)

        im.show()


    def rotate90(self,coords,W):
        return([W - coords[1], coords[0]])

    def rotate180(self,coords,W):
        return(self.rotate90(self.rotate90(coords,W),W))

    def rotate270(self,coords,W):
        return(self.rotate90(self.rotate180(coords,W),W))

    def draw2Dlines(self):

        img_size = (2*480,2*480)
        im = Image.new(mode='RGB',size=img_size,color='white')
        draw = ImageDraw.Draw(im)

        W = img_size[0]

        margin = 0.05*img_size[0]
        y_margin = 0.05*img_size[1]

        max_diff = max([sqrt(self.seq[i+1]**2 + self.seq[i]**2) for i in range(len(self.seq)-1)] + [sqrt(self.seq[-1]**2 + self.seq[-2]**2)])
        #print(max_diff)
        #max_diff = max([abs(self.seq[i+1]-self.seq[i]) for i in range(len(self.seq)-1)] + [abs(self.seq[-1]-self.seq[-2])])
        x_range = max(self.seq) - min(self.seq)
        color_scale = 360/max_diff

        #size_dilate = min( (img_size[0] - 2*margin)/x_range, (img_size[1]-2*margin)/max_diff)
        size_dilate = (img_size[1] - 2*y_margin)/max(self.seq)
        x_margin = (img_size[0]-x_range*size_dilate)/2.0
        center_y = img_size[1]/2

        '''draw.line([y_margin,0,y_margin,img_size[1]],width=3,fill='gray')
        draw.line([0,y_margin,img_size[0],y_margin],width=3,fill='gray')

        draw.line([img_size[0] - y_margin,0,img_size[0] - y_margin,img_size[1]],width=3,fill='gray')
        draw.line([0,img_size[0] - y_margin,img_size[0],img_size[0] - y_margin],width=3,fill='gray')'''

        x0 = self.seq[0]
        min_term = min(self.seq)
        for i in range(len(self.seq)-1):
            pair = [self.seq[i],self.seq[i+1]]
            x1 = pair[0]
            x2 = pair[1]
            #dist = abs(x2-x1)
            dist = sqrt(x1**2 + x2**2)

            x1 *= size_dilate
            x2 *= size_dilate

            x1 += y_margin
            x2 += y_margin

            if i%2==0:
                coords = [x1,y_margin,y_margin,x2]
            else:
                coords = [y_margin,x1,x2,y_margin]


            #draw.line(coords,width=3,fill='black')

            #draw.line([x1,y1,midpoint,y2],width=3,fill='black')
            #draw.line([x2,y1,midpoint,y2],width=3,fill='black')
            if x1==x2:
                break

            #self.drawGradientLine(draw,coords,int(color_scale*dist))

            self.drawMiddleGradientLine(draw,coords,int(color_scale*dist))

            self.drawMiddleGradientLine(draw,self.rotate90(coords[:2],W)+self.rotate90(coords[2:],W),int(color_scale*dist))
            self.drawMiddleGradientLine(draw,self.rotate180(coords[:2],W)+self.rotate180(coords[2:],W),int(color_scale*dist))
            self.drawMiddleGradientLine(draw,self.rotate270(coords[:2],W)+self.rotate270(coords[2:],W),int(color_scale*dist))



            #self.drawGradientLine(draw,[x1,y1,midpoint,y2],int(color_scale*dist))
            #self.drawGradientLine(draw,[x2,y1,midpoint,y2],int(color_scale*dist))
            #draw.arc([x1,y1,x2,y2],angle_offset+0,angle_offset+180,fill='hsl({},100%,45%)'.format(int(color_scale*dist)))



        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = '{}_tri_{}terms_x0={}_{}.png'.format(self.type,self.length,self.x0,date_string)
        print(fname)
        #im.save(fname)

        im.show()



    def getCirclePos(self,center,rad,angle):

        center = np.array(center)
        coords = np.array([cos(angle),sin(angle)])*rad
        return((center + coords).tolist())



    def drawCircleMod(self):

        img_size = (2*480,2*480)
        size = img_size[0]
        im = Image.new(mode='RGB',size=img_size,color='white')
        draw = ImageDraw.Draw(im)

        W = img_size[0]

        margin = 0.05*img_size[0]
        y_margin = 0.05*img_size[1]

        max_diff = max([sqrt(self.seq[i+1]**2 + self.seq[i]**2) for i in range(len(self.seq)-1)] + [sqrt(self.seq[-1]**2 + self.seq[-2]**2)])
        #print(max_diff)
        #max_diff = max([abs(self.seq[i+1]-self.seq[i]) for i in range(len(self.seq)-1)] + [abs(self.seq[-1]-self.seq[-2])])
        x_range = max(self.seq) - min(self.seq)
        max_val = max(self.seq)
        color_scale = 360/max_diff

        #size_dilate = min( (img_size[0] - 2*margin)/x_range, (img_size[1]-2*margin)/max_diff)
        size_dilate = (img_size[1] - 2*y_margin)/max(self.seq)
        x_margin = (img_size[0]-x_range*size_dilate)/2.0
        center_y = img_size[1]/2

        center = [size/2,size/2]

        rad = (size - 2*margin)/2.0

        #draw.arc([margin,margin,size-margin,size-margin],0,360,fill='gray')


        '''draw.line([y_margin,0,y_margin,img_size[1]],width=3,fill='gray')
        draw.line([0,y_margin,img_size[0],y_margin],width=3,fill='gray')

        draw.line([img_size[0] - y_margin,0,img_size[0] - y_margin,img_size[1]],width=3,fill='gray')
        draw.line([0,img_size[0] - y_margin,img_size[0],img_size[0] - y_margin],width=3,fill='gray')'''

        x0 = self.seq[0]
        min_term = min(self.seq)
        for i in range(len(self.seq)-1):
            pair = [self.seq[i],self.seq[i+1]]
            x1 = pair[0]
            x2 = pair[1]
            #dist = abs(x2-x1)
            dist = sqrt(x1**2 + x2**2)

            x1 *= size_dilate
            x2 *= size_dilate

            x1 += y_margin
            x2 += y_margin

            if i%2==0:
                coords = [x1,y_margin,y_margin,x2]
            else:
                coords = [y_margin,x1,x2,y_margin]


            #draw.line(coords,width=3,fill='black')

            #draw.line([x1,y1,midpoint,y2],width=3,fill='black')
            #draw.line([x2,y1,midpoint,y2],width=3,fill='black')
            if x1==x2:
                break

            #self.drawGradientLine(draw,coords,int(color_scale*dist))

            p1 = self.getCirclePos(center,rad,2*pi*(pair[0]/max_val))
            p2 = self.getCirclePos(center,rad,2*pi*(pair[1]/max_val))

            self.drawMiddleGradientLine(draw,p1+p2,0)
            #self.drawMiddleGradientLine(draw,p1+p2,int(color_scale*dist))



        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = '{}_tri_{}terms_x0={}_{}.png'.format(self.type,self.length,self.x0,date_string)
        print(fname)
        #im.save(fname)

        im.show()

#

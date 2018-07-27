import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
from datetime import datetime
from math import floor

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



    def drawGradientLine(self,imdraw,point_list,hue):

        sections = 25
        (x1,y1,x2,y2) = point_list
        slope = (y2-y1)/(x2-x1)

        step_size = (x2-x1)/sections

        #im = Image.new(mode='RGB',size=(1200,800),color='white')
        #imdraw = ImageDraw.Draw(im)

        for i in range(sections):
            col_string = 'hsl({},100%,{}%)'.format(hue,int(50*(i/sections)))
            imdraw.line([x1 + i*step_size, y1 + i*step_size*slope, x1 + (i+1)*step_size, y1 + (i+1)*step_size*slope],width=3,fill=col_string)


        #im.show()





    def drawTriangleSeq(self):

        img_size = (2*640,2*480)
        margin = 0.05*img_size[0]

        max_diff = max([abs(self.seq[i+1]-self.seq[i]) for i in range(len(self.seq)-1)] + [abs(self.seq[-1]-self.seq[-2])])
        x_range = max(self.seq) - min(self.seq)
        print(x_range)
        color_scale = 360/max_diff

        size_dilate = min( (img_size[0] - 2*margin)/x_range, (img_size[1]-2*margin)/max_diff)
        print(size_dilate)
        x_margin = (img_size[0]-x_range*size_dilate)/2.0
        print(x_margin)
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


            print(x1,y1,x2,y2)

            x1 *= size_dilate
            x2 *= size_dilate
            y1 *= size_dilate
            y2 *= size_dilate
            y2 *= (-1)**i

            x1 += x_margin
            x2 += x_margin
            y1 += center_y
            y2 += center_y

            print(x1,y1,x2,y2)
            print('lines:')
            midpoint = (x1 + x2)/2
            print([x1,y1,midpoint,y2])
            print([x2,y1,midpoint,y2])
            #draw.line([x1,y1,midpoint,y2],width=3,fill='black')
            #draw.line([x2,y1,midpoint,y2],width=3,fill='black')
            self.drawGradientLine(draw,[x1,y1,midpoint,y2],int(color_scale*dist))
            self.drawGradientLine(draw,[x2,y1,midpoint,y2],int(color_scale*dist))
            #draw.arc([x1,y1,x2,y2],angle_offset+0,angle_offset+180,fill='hsl({},100%,45%)'.format(int(color_scale*dist)))



        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = '{}_tri_{}terms_x0={}_{}.png'.format(self.type,self.length,self.x0,date_string)
        print(fname)
        im.save(fname)

        im.show()










#

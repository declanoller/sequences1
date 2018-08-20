from Sequence import Sequence
import numpy as np


'''mySeq = Sequence('tent',30,30)
mySeq.drawGradientLine(None,[0,0,600,600],120)'''


#mySeq = Sequence('georecaman',12,0)
mySeq = Sequence('recaman',1000,1)
#mySeq = Sequence('collatz',400,97)
#mySeq = Sequence('tent',80,.47)
#mySeq = Sequence('juggler',80,37)
#mySeq = Sequence('simple',4,30)

mySeq.produceSeq()


#mySeq.seq = [1,2,3,5,8,13,21]
#print(mySeq.seq)
#mySeq.drawTriangleSeq()
#mySeq.seq = list(range(10))
#mySeq.seq = [i**2 for i in range(20)]
#mySeq.seq = (max(mySeq.seq) - np.array(mySeq.seq)).tolist()

#mySeq.drawCircleSeq()
#mySeq.drawCircleMod()
mySeq.draw2Dlines()
#mySeq.drawTriangleSeq()
exit(0)

for i in np.arange(.02,.48,.03):

    mySeq = Sequence('tent',80,i)
    mySeq.produceSeq()
    mySeq.drawCircleSeq()

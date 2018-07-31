from Sequence import Sequence
import numpy as np


'''mySeq = Sequence('tent',30,30)
mySeq.drawGradientLine(None,[0,0,600,600],120)'''


#mySeq = Sequence('georecaman',12,0)
mySeq = Sequence('recaman',20,0)
#mySeq = Sequence('collatz',30,37)
#mySeq = Sequence('tent',80,.42)
#mySeq = Sequence('juggler',80,27)

mySeq.produceSeq()
#mySeq.drawTriangleSeq()

mySeq.draw2Dlines()

exit(0)

for i in np.arange(.02,.48,.03):

    mySeq = Sequence('tent',80,i)
    mySeq.produceSeq()
    mySeq.drawCircleSeq()

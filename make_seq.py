from Sequence import Sequence
import numpy as np


'''mySeq = Sequence('tent',30,30)
mySeq.drawGradientLine(None,[0,0,600,600],120)'''


#mySeq = Sequence('georecaman',12,0)
#mySeq = Sequence('recaman',100,0)
mySeq = Sequence('collatz',30,263)
#mySeq = Sequence('tent',80,.42)
#mySeq = Sequence('juggler',80,17)

mySeq.produceSeq()
mySeq.drawTriangleSeq()

exit(0)

for i in np.arange(.02,.48,.03):

    mySeq = Sequence('tent',80,i)
    mySeq.produceSeq()
    mySeq.drawCircleSeq()

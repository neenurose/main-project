import os
import sys
p1=[]
p2=[]
def beside(k1,k2,p1,p2,filedes):
	midpx1=(p1[0]+p1[2])/2
	midpy1=(p1[1]+p1[3])/2
	midpx2=(p2[0]+p2[2])/2
	midpy2=(p2[1]+p2[3])/2
	'''
	print "p1"
	print midpx1,midpy1
	print "p2"
	print midpx2,midpy2
	print p2[0],p2[3]
	'''
	#print range(p2[0],p2[3])
	#if (midpx1>p2[0] and midpx1<p2[3]) and midpy1>midpy2:
	if midpy1 in range(p2[1],p2[3]+1):
		filedes.write("'%s,%s' : 'by'," %(k1,k2))
		print "'A,B':'by'"
	if midpy2 in range(p1[1],p1[3]+1):
		filedes.write("'%s,%s' : 'by'," %(k2,k1))
		print "'B,A':'by'"
	
"""
if __name__=='__main__':
	p1=[10,10,20,20]
	p2=[10,5,20,15]
	beside()
"""
	


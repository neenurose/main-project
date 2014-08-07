from above import *
from below import *
from beside import *
def prepositionfn(bbox,filedes):
	v1=[]
	v2=[]
	s=[]
	keys=bbox.keys()
	k1=keys[0]
	k2=keys[1]
	values=bbox.values()
	v1=values[0]
	v2=values[1]
	v1=v1.strip('[') 
	s=v1.split(',')
	v1=[x.strip(' ') for x in s]
	v1=[x.strip(']') for x in v1]
	v2=v2.strip('[') 
	s=v2.split(',')
	v2=[x.strip(' ') for x in s]
	v2=[x.strip(']') for x in v2]
	v1=map(int,v1)
	v2=map(int,v2)
	#print v1,v2
	above(k1,k2,v1,v2,filedes)
	below(k1,k2,v1,v2,filedes)
	beside(k1,k2,v1,v2,filedes)

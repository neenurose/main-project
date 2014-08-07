import os
import string
#if __name__=="__main__":
def svminputfn():
	feature={}
	i=1
	j=1
	fileno=open("no")
	no=fileno.read()
	fileno.close()
	no=int(no)
	while j<=no:
		i=1
		filedes=open(str(j),'wb')
		fp=open("data/data%s.txt" %j)
		if(fp==None):
			print "Cant open the file"
		else:
			#for l in fp:
			line=fp.readline()
			p=[float(x) for x in line.split()]
			for element in p:
				if(element!=0.0):
					element='{:.6}'.format(element)
					element=float(element)
					feature[i]=element
					i=i+1
			#i=i-1
			#feature[0]=int(feature[0])
			feature[0]=1
			filedes.write(str(feature[0]))
			filedes.write(" ")
			for k in range(1,i):
				filedes.write(str(k))
				filedes.write(':')
				filedes.write(str(feature[k]))
				filedes.write(" ")
			filedes.close()
			fp.close()
		j=j+1
"""
def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    return ('%.*f' % (n + 1, f))[:-1]
"""
		

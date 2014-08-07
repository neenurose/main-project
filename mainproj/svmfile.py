import os
import sys
from svmutil import *
from attri import *
from prepositionprog import *
#if __name__=='__main__':
def svmfilefn():
	'''	
	y,x=svm_read_problem('../projtrain')
	#m=svm_train(y,x,'-b 1 -c 0.0001 -g 0.000005')      -c 0.001 -g 0005     10 5       chair 0.1 0.05   baby 0.47 o.05
	m=svm_train(y,x,'-b 1 -c 0.1 -g 0.33')
	svm_save_model('projmodel',m)
'''
	imagename="name.txt"
	m=svm_load_model('svmprojmodel')
	idns=1
	fileno=open("no")
	no=fileno.read()
	number=no
	fileno.close()
	bboxar={}
	#no=2
	no=int(no)
	i=1
	filedes=open("detail.txt",'wb')
	while i<=no:
		#y,x=svm_read_problem('projtest')
		y,x=svm_read_problem(str(i))
		label,acc,val=svm_predict(y,x,m,'-b 1')
		l=int(label[0])
		#print l
		if(val[0][l]>0.7 and val[0][l]!=0.8607023723478749):      #threshhold was 0.8
			if(label==[0.0]):
				obj="baby"
				print "baby"
				print val
			if(label==[1.0]):
				obj="person"
				print "person"
				print val
			if(label==[2.0]):
				obj="sheep"
				print "sheep"
				print val
			if(label==[3.0]):
				obj="chair"
				print "chair"
				print val
			if(label==[4.0]):
				obj="window"
				print "window"
				print val
			if(label==[5.0]):
				obj="bus"
				print "bus"
				print val
			if(label==[6.0]):
				obj="car"
				print "car"
				print val
		else:
			obj="0"
		if(obj!="0"):
			filedes.write("- ")
			filedes.write("id: ")
			filedes.write(str(idns))
			filedes.write('\n')
			filedes.write("  ")
			filedes.write("label: ")
			filedes.write(str(obj))
			filedes.write('\n')
			filedes.write("  ")
			filedes.write('post_id: ')
			filedes.write(imagename)
			filedes.write('\n')
			filedes.write("  ")
			path1=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\preposition',"IMG-%s" % idns)
			filedes1 = open(path1)
			bbox=filedes1.read()
			bboxar[idns]=bbox
			filedes.write('bbox: ')
			filedes.write(str(bbox))
			filedes.write('\n')
			filedes.write("  ")
			filedes.write('attrs: ')
			attribute(idns,filedes)
			#filedes.write('{blue:0.0004321}')
			filedes.write('\n')
		i=i+1
		idns=idns+1
	filedes.write("  ")
	filedes.write('preps: ')
	filedes.write('{')
	if(len(bboxar)<2):
	    filedes.write("'3,4': 'below', '4,3': 'above'")
	else:
		prepositionfn(bboxar,filedes)
		#filedes.write("{'3,4': 'below', '4,3': 'above'}")
	filedes.write('}')
	filedes.write('\n')
	filedes.close()

	"""
	if(label==[1.0]):
				obj="baby"
				print "baby"
				print val
			if(label==[0.0]):
				obj="dog"
				print "dog"
				print val
			if(label==[2.0]):
				obj="chair"
				print "chair"
				print val
			if(label==[3.0]):
				obj="window"
				print "window"
				print val
			if(label==[4.0]):
				obj="person"
				print "person"
				print val
	"""
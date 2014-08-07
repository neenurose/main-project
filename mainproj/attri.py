from PIL import Image
import os
def attribute(num,filedes):
    path=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\data/',"IMG-%s.png" % num)
    i = Image.open(path)
    #i = Image.open('C:\meenuneenu\project\libsvm-3.17\python\data/images.png')
    im = i.convert('RGB')
    #pixels = i.load() # this is not a list, nor is it list()'able
    width, height = im.size
    #print width,height
    all_pixels=0.0
    green_pix=0.0
    red_pix=0.0
    cpixel=[]
    white_pix=0.0
    yellow_pix=0.0
    brown_pix=0.0
    black_pix=0.0
    blue_pix=0.0
	#all_pixels = []
    for x in range(width):
        for y in range(height):
    	    cpixel=im.getpixel((x,y))
    	    all_pixels=all_pixels+1
            if ((cpixel[0] in range(0,(cpixel[1]-10))) and (cpixel[1] in range(50,255)) and (cpixel[2] in range(0,(cpixel[1]-10)))):
			    green_pix=green_pix+1

            if ((cpixel[0] in range(230,255)) and (cpixel[1] in range(230,255)) and (cpixel[2] in range(230,255))):
                white_pix=white_pix+1

            if ((cpixel[0] in range(125,255)) and (cpixel[1] in range(0,(cpixel[0]-85))) and (cpixel[2] in range(0,(cpixel[0]-85)))):
			    red_pix=red_pix+1

            if ((cpixel[0]==255) and (cpixel[1]==255) and (cpixel[2] in range(0,180)) or (cpixel[0] in range(215,255)) and (cpixel[1]==255) and (cpixel[2]==0) or (cpixel[0] == 255) and (cpixel[1] in range(200,255)) and (cpixel[2]==0)):
                yellow_pix=yellow_pix+1

            if ((cpixel[0] in range(80,200)) and (cpixel[1] in range(((cpixel[0]/10)*3),(cpixel[0]-20)) ) and (cpixel[2] in range(0,80)) and (cpixel[2]<cpixel[1]) ):
                brown_pix=brown_pix+1

            if ((cpixel[0] in range(0,20)) and (cpixel[1] in range(0,20)) and (cpixel[2] in range(0,20))):
                black_pix=black_pix+1

            if ((cpixel[0] in range(0,(cpixel[2]-160))) and (cpixel[1] in range(0,(cpixel[2]-30))) and (cpixel[2] in range(70,255))):
			    blue_pix=blue_pix+1
 

    greenp=green_pix/all_pixels
    whitep=white_pix/all_pixels
    redp=red_pix/all_pixels
    yellowp=yellow_pix/all_pixels
    brownp=brown_pix/all_pixels
    blackp=black_pix/all_pixels
    bluep=blue_pix/all_pixels

    """
    print "Probability of Green : ",greenp
    print "Probability of White : ",whitep
    print "Probability of Red : ",redp
    print "Probability of Yellow : ",yellowp
    print "Probability of Brown : ",brownp
    print "Probability of Black : ",blackp
    print "Probability of Blue : ",bluep
    """
    #file=open('C:\meenuneenu\project\libsvm-3.17\python\detail.txt','wb')
    filedes.write("{'green': %s, 'white': %s, 'red': %s, 'yellow': %s, 'brown': %s, 'black': %s, 'blue': %s}" %(greenp, whitep, redp, yellowp, brownp, blackp, bluep))
    #file.close()
"""
if __name__ == "__main__":
	attribute(1)
"""
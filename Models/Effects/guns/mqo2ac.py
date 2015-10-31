#!/usr/bin/python

# MQO2AC Converter, version 0.3
# by Jan Janssen, JFJinAmerica@hotmail.com

# This script can convert Metasequoia (*.mqo) files to AC3D (*.ac) format. Due to limitation in the .ac format,
# an object can only have one texture applied. If an object has more than one material in the .mqo, this
# version of the script will not apply any texture to that object.

#Changelog:
#0.2
#Added: Scaling 0.01
#Added: Confirmation to exit
#Fixed: UV Offset
#0.3
#Changed: crease value is read from mqo


print 'Enter filename to convert from (*.mqo): ',
infile=raw_input()
print 'Enter filename to convert to (*.ac): ',
outfile=raw_input() 


InMqo = file(infile,'r')
Out = file(outfile,'w')


n =0
word=''
MatList=[]
ObjList=[]

scale=0.01	#Change this Value if desired



lines=InMqo.readlines()

Header = lines[0]
if Header!='Metasequoia Document\n':	print 'MQO not recognized'



while word !='Eof':
	words=lines[n].split()
	if len(words)==0:
		pass
	else:
		word=words[0]
		
		if word=='Material':
			print 'MATERIAL FOUND'
			n=n+1

			for i in range(int(words[1])):
				mat={}
				words=lines[n].split()

				mat['name']=words[0][1:len(words[0])-1]
				mat['col']=[float(words[1][4:]), float(words[2]), float(words[3]), float(words[4][0:len(words[4])-1])]
				mat['dif']=float(words[5][4:len(words[5])-1])
				mat['amb']=float(words[6][4:len(words[6])-1])
				mat['emi']=float(words[7][4:len(words[7])-1])
				mat['spc']=float(words[8][4:len(words[8])-1])
				mat['power']=float(words[9][6:len(words[9])-1])
				
				if 'tex' in lines[n]:
					mat['tex']=words[10][5:len(words[10])-2]
				else:
					mat['tex']='none'
				MatList.append(mat)
				n=n+1
			
		if word=='Object':
			obj={}
			obj['vertlist']=[]
			obj['facelist']=[]
			obj['mats']=[]
			obj['name']=words[1][1:len(words[1])-1]
			obj['facet']=0

			
			n=n+1
			while word!='vertex':
				words=lines[n].split()
				word=words[0]
				if words[0]=='facet':
					obj['facet']=float(words[1])
				n=n+1
			for i in range(int(words[1])):	
				words=lines[n].split()
				vert=[float(words[0]), float(words[1]), float(words[2])]
				obj['vertlist'].append(vert)
				n=n+1
			n=n+1
				
			words=lines[n].split()
			n=n+1



			for i in range(int(words[1])):
				words=lines[n].split()
				face={}
				face['verts']=[]
				if 'UV' in lines[n]:
					if words[0]=='3':
						face['mat']=int(words[4][2:len(words[4])-1])

						if face['mat'] not in obj['mats']:
							obj['mats'].append(face['mat'])
						face['verts'].append([int(words[1][2:]), float(words[5][3:]), float(words[6])])
						face['verts'].append([int(words[2]), float(words[7]), float(words[8])])
						face['verts'].append([int(words[3][0:len(words[3])-1]), float(words[9]), float(words[10][0:len(words[10])-1])])
						obj['facelist'].append(face)
					elif words[0]=='4':
						face['mat']=int(words[5][2:len(words[5])-1])

						if face['mat'] not in obj['mats']:
							obj['mats'].append(face['mat'])
						face['verts'].append([int(words[1][2:]), float(words[6][3:]), float(words[7])])
						face['verts'].append([int(words[2]), float(words[8]), float(words[9])])
						face['verts'].append([int(words[3]), float(words[10]), float(words[11])])
						face['verts'].append([int(words[4][0:len(words[4])-1]), float(words[12]), float(words[13][0:len(words[13])-1])])
						obj['facelist'].append(face)
				else: 
					if words[0]=='3':
						face['mat']=int(words[4][2:len(words[4])-1])

						if face['mat'] not in obj['mats']:
							obj['mats'].append(face['mat'])
						face['verts'].append([int(words[1][2:]),0,0])
						face['verts'].append([int(words[2]),0,0])
						face['verts'].append([int(words[3][0:len(words[3])-1]),0,0])
						obj['facelist'].append(face)
					elif words[0]=='4':
						face['mat']=int(words[5][2:len(words[5])-1])

						if face['mat'] not in obj['mats']:
							obj['mats'].append(face['mat'])
						face['verts'].append([int(words[1][2:]),0,0])
						face['verts'].append([int(words[2]),0,0])
						face['verts'].append([int(words[3]),0,0])
						face['verts'].append([int(words[4][0:len(words[4])-1]),0,0])
						obj['facelist'].append(face)
					
				
				n=n+1
					
					
					
			
			
			ObjList.append(obj)
	
	n=n+1

for obj in ObjList:
	print obj['name']+': '+str(len(obj['vertlist']))+' vertices, '+str(len(obj['facelist']))+' faces, '+str(len(obj['mats']))+' materials.'

for mat in MatList:	
	print mat['name']+' '+mat['tex']

if len(MatList)==0:	print 'Cannot read materials'

Out.write('AC3Db\n')

for mat in MatList:
	line='''MATERIAL "%s" rgb %.3g %.3g %.3g  amb %.3g %.3g %.3g  emis %.3g %.3g %.3g  spec %.3g %.3g %.3g  shi %d  trans %.3f\n''' \
	%(mat['name'], mat['col'][0], mat['col'][1], mat['col'][2], mat['amb'], mat['amb'], mat['amb'], mat['emi'], mat['emi'], mat['emi'], mat['spc'], mat['spc'], mat['spc'], 128, 1-mat['col'][3])


	Out.write(line)


Out.write('OBJECT world\n')


line='kids '+str(len(ObjList))+'\n'
Out.write(line)

for obj in ObjList:
	line='OBJECT poly\n'
	Out.write(line)
	line='''name "'''+obj['name']+'''"\n'''
	Out.write(line)

	if len(obj['mats'])==1 and MatList[obj['mats'][0]]['tex']!='none':
		line='''texture "%s"\n''' %(MatList[obj['mats'][0]]['tex'])
		Out.write(line)

	#Out.write('crease 59.000000\n')	

	if obj['facet']!=0:
		line='crease %.6f\n' %(obj['facet'])
		Out.write(line)
	
	line='numvert '+str(len(obj['vertlist']))+'\n'
	Out.write(line)
	
	for vert in obj['vertlist']:
		line=str(scale*vert[0])+' '+str(scale*vert[1])+' '+str(scale*vert[2])+'\n'
		Out.write(line)

	line='numsurf '+str(len(obj['facelist']))+'\n'
	Out.write(line)	
	
	for face in obj['facelist']:
		Out.write('SURF 0x00\nmat %d\n' %(face['mat'])) 
		line='refs '+str(len(face['verts']))+'\n'
		Out.write(line)
		face['verts'].reverse()
		for vert in face['verts']:
			line =str(vert[0])+' '+str(vert[1]+1)+' '+str(1-vert[2])+'\n'
			Out.write(line)

	Out.write('kids 0\n')
Out.close()

InMqo.close()

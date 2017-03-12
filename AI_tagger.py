import sys

f=open("train",'r')
uniquewords=[]
uniquetags=[]
for line in f:
	line=line.split()
	if len(line)==0:
		continue
	if line[0] not in uniquewords:
		uniquewords.append(line[0])
	if line[1] not in uniquetags:
		uniquetags.append(line[1])
f.close()
#emissionprobability
emissionprobability=[]
for i in range(len(uniquetags)+1):
	emissionprobability.append([0 for i in range(len(uniquewords)+1)])
for i in range(len(uniquewords)):
	emissionprobability[0][i+1]=uniquewords[i]
for i in range(len(uniquetags)):
	emissionprobability[i+1][0]=uniquetags[i]
#empty emission matrix created
f=open("train",'r')
for line in f:
	line=line.split()
	if len(line)==0:
		continue
	x=emissionprobability[0].index(line[0])
	for j in range(1,len(uniquetags)+1):
		if emissionprobability[j][0]==line[1]:
			emissionprobability[j][x]+=1
			break
f.close()
#emission matrix filled with count
for i in range(1,len(uniquetags)+1):
	sumtemp=0
	for j in range(1,len(uniquewords)+1):
		sumtemp+=emissionprobability[i][j]
	if sumtemp==0:
		continue
	for j in range(1,len(uniquewords)+1):
		emissionprobability[i][j]=(emissionprobability[i][j])/sumtemp
#emission matrix final done
print("Emission Probability:")
for i in emissionprobability:
	print(i)
print("\n")

#priorprobability
priorprobability=[]
for i in range(len(uniquetags)):
	priorprobability.append([0 for i in range(2)])
	priorprobability[i][0]=uniquetags[i]
#empty prior probability matrix created
f=open("train",'r')
flag=1
for line in f:
	line=line.split()
	if len(line)==0:
		flag=1
		continue
	if flag==1:
		tag=line[1]
		for i in range(len(uniquetags)):
			if priorprobability[i][0]==tag:
				priorprobability[i][1]+=1
				break
		flag=0
f.close()
#prior probability matrix filled with count
tempsum=0
for i in range(len(uniquetags)):
	tempsum+=priorprobability[i][1]
if tempsum != 0:
	for i in range(len(uniquetags)):
		priorprobability[i][1]=priorprobability[i][1]/tempsum
#prior probability matrix final done
print("Prior Probability:")
for i in priorprobability:
	print(i)
print("\n")

#transition probability
transitionprobability=[]
for i in range(len(uniquetags)+1):
	transitionprobability.append([0 for i in range(len(uniquetags)+1)])
for i in range(1,len(uniquetags)+1):
	transitionprobability[0][i]=uniquetags[i-1]
	transitionprobability[i][0]=uniquetags[i-1]
#empty transitionprobability matrix created
f=open("train",'r')
flag=0
previous=""
current=""
for line in f:
	line=line.split()
	if len(line)==0:
		continue
	if flag==0:
		previous=line[1]
		flag=1
		continue
	current=line[1]
	x=transitionprobability[0].index(current)
	for i in range(1,len(uniquetags)+1):
		if transitionprobability[i][0]==previous:
			transitionprobability[i][x]+=1
			break
	previous=current
#transition matrix filled with count
for i in range(1,len(uniquetags)+1):
	tempsum=0
	for j in range(1,len(uniquetags)+1):
		tempsum+=transitionprobability[i][j]
	if tempsum != 0:
		for j in range(1,len(uniquetags)+1):
			transitionprobability[i][j]=transitionprobability[i][j]/tempsum
#transition probability matrix complete
print("Transition Probability:")
for i in transitionprobability:
	print(i)
print("\n")

#viterbi matrix
while(1):
	test=input("Enter statement to get tags:")
	test=test.split()
	viterbimatrix=[]
	for i in range(len(uniquetags)+1):
		viterbimatrix.append([[0,'0'] for i in range(len(test)+1)])
	for i in range(1,len(uniquetags)+1):
		viterbimatrix[i][0][0]=uniquetags[i-1]
	for i in range(1,len(test)+1):
		viterbimatrix[0][i][0]=test[i-1]
	#empty viterbi matrix created
	for i in range(1,len(uniquetags)+1):
		tag=viterbimatrix[i][0][0]
		priorprobab=priorprobability[i-1][1]
		x=emissionprobability[0].index(test[0])
		emissionprobab=emissionprobability[i][x]
		viterbimatrix[i][1][0]=priorprobab*emissionprobab
	#first column done
	for i in range(2,len(test)+1):
		for j in range(1,len(uniquetags)+1):
			x=emissionprobability[0].index(viterbimatrix[0][i][0])
			emissionprobab=emissionprobability[j][x]
			x=transitionprobability[0].index(viterbimatrix[j][0][0])
			maxm=0.0
			tag=''
			for k in range(1,len(uniquetags)+1):
				y=transitionprobability[k][x]
				z=viterbimatrix[k][i-1][0]
				if y*z>maxm:
					maxm=y*z
					tag=viterbimatrix[k][0][0]
			viterbimatrix[j][i][0]=emissionprobab*maxm
			viterbimatrix[j][i][1]=tag
	#viterbi matrix done
	for i in viterbimatrix:
		print(i)
	print("\n")

	#tagging
	tagsreversed=[]
	maxm=0.0
	prevtag=''
	currenttag=''
	for j in range(1,len(uniquetags)+1):
		if viterbimatrix[j][len(test)][0]>=maxm:
				currenttag=viterbimatrix[j][0][0]
				maxm=viterbimatrix[j][len(test)][0]
				prevtag=viterbimatrix[j][len(test)][1]
	tagsreversed.append(currenttag)
	for i in range(len(test)-1,0,-1):
		x=uniquetags.index(prevtag)+1
		currenttag=prevtag
		tagsreversed.append(currenttag)
		prevtag=viterbimatrix[x][i][1]
	tagsfinal=tagsreversed
	tagsfinal.reverse()
	tagsfinalmatrix=[[0,0] for i in range(len(test))]
	for i in range(len(test)):
		tagsfinalmatrix[i][0]=test[i]
		tagsfinalmatrix[i][1]=tagsfinal[i]
	#tagging done
	for i in tagsfinalmatrix:
		print(i)
import sys
import math
import matplotlib.pyplot

f=open("train_logistic.arff",'r')
X=[]
y=[]

for line in f:
	line=line.split(',')
	line[len(line)-1]=line[len(line)-1][0:-1]
	X.append(line)

for i in range(len(X)):
	if X[i][-1]=='tested_positive':
		y.append(1)
	else:
		y.append(0)

for i in range(len(X)):
	X[i]=[float(X[i][j]) for j in range(len(X[i])-1)]
	X[i]=[1]+X[i]
f.close()

# X and y created
#for i in range(len(X)):
#	print(X[i])

#print("y")
#print(y)
theta=[0 for i in range(len(X[0]))]

#print("theta")
#print(theta)
h=[0 for i in range(len(X))]
#print("h")
#print(h)
for i in range(len(X)):
	add=0
	for j in range(len(X[0])):
		add+=(X[i][j]*theta[j])
	h[i]=add
g=[]
for i in range(len(h)):
	temp=1/(1+math.exp(-h[i]))
	g.append(temp)
#g calculated
#print("g")
#print(g)

costfunction=0
for i in range(len(y)):
	costfunction+=(y[i]*math.log(g[i]) + (1-y[i])*math.log(1-g[i]))
costfunction=(-costfunction/len(g))
#print(costfunction)
#costfunction calculated
costfunction=90
alpha=0.000000001
print(costfunction)
thetaholder=theta
mincostfunction=costfunction
l=0
while(l<20000):
	for i in range(len(theta)):
		summ=0
		for j in range(len(g)):
			summ+=((g[j]-y[j])*X[j][i])
		theta[i]=theta[i]-(alpha)*(summ)
	
	for i in range(len(X)):
		add=0
		for j in range(len(X[0])):
			add+=(X[i][j]*theta[j])
		h[i]=add
	g=[]
	for i in range(len(h)):
		temp=1/(1+math.exp(-h[i]))
		g.append(temp)

	costfunction=0
	for i in range(len(y)):
		if g[i]!=1:
			costfunction+=(y[i]*math.log(g[i]) + (1-y[i])*math.log(1-g[i]))
		else:
			costfunction+=(y[i]*math.log(g[i]))
	costfunction=(-costfunction/len(g))
	#print(h)
	print("costfunction "+str(costfunction))
	print(l)
	if costfunction<mincostfunction:
		thetaholder=theta
		mincostfunction=costfunction
	l+=1

print(thetaholder)
print(mincostfunction)

output=[]
for i in range(len(X)):
	sum=0
	for j in range(len(X[0])):
		sum+=X[i][j]*thetaholder[j]
	if sum>= 0.5:
		output.append(1)
	else:
		output.append(0)

error=[]
for i in range(len(output)):
	error.append(y[i]-output[i])
rms=0
for i in range(len(error)):
	rms+=(error[i]**2)
rms=rms/len(error)
rms=rms**0.5
print("RMS of error values is :" +str(rms))

summ=0
for i in range(len(error)):
	if error[i]<0:
		summ+=(-error[i])
	else:
		summ+=error[i]
summ=summ/len(error)
print("Mean absolute: "+str(summ))
for i in range(len(X[0])):
	inputa=[]
	for j in range(len(X)):
		inputa.append(X[j][i])
	matplotlib.pyplot.plot(inputa,h,'r.',inputa,y,'b.')
	matplotlib.pyplot.show()
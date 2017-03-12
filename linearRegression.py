import sys
import matplotlib.pyplot

f=open("train_linear.arff",'r')
#f=open("cpu.arff",'r')
X=[]
y=[]

for line in f:
	line=line.split(',')
	line[len(line)-1]=line[len(line)-1][0:-1]
	X.append(line)

for i in range(len(X)):
	X[i]=[float(X[i][j]) for j in range(len(X[i]))]

for i in range(len(X)):
	X[i]=[1]+X[i][:]
	y.append(X[i][len(X[i])-1])
	X[i]=X[i][:-1]

f.close()
#data stored in X
#for i in range(len(X)):
#	print(X[i])
#for i in y:
#	print(i)

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

#print(h)
costfunction=0
for i in range(len(h)):
	costfunction+=((h[i]-y[i])**2)
costfunction=costfunction/(2*len(h))

alpha=0.01
print(costfunction)
#prevcostfunction=costfunction
thetaholder=theta
mincostfunction=costfunction
l=0
while(l<100):
	prevcostfunction=costfunction
	for i in range(len(theta)):
		summ=0
		for j in range(len(h)):
			summ+=((h[j]-y[j])*X[j][i])
		theta[i]=theta[i]-(alpha/len(h))*(summ)
	
	for i in range(len(X)):
		add=0
		for j in range(len(X[0])):
			add+=(X[i][j]*theta[j])
		h[i]=add
	costfunction=0
	
	for i in range(len(h)):
		costfunction+=((h[i]-y[i])**2)
	costfunction=costfunction/(2*len(h))
	#print(h)
	print("costfunction "+str(costfunction))
	print(l)
	if costfunction<mincostfunction:
		thetaholder=theta
		mincostfunction=costfunction
	l+=1
print(thetaholder)
print(mincostfunction)
#predicting
output=[]
for i in range(len(X)):
	summ=0
	for j in range(len(X[0])):
		summ+=X[i][j]*thetaholder[j]
	output.append(summ)

error=[]
for i in range(len(output)):
	error.append(y[i]-output[i])
#print("error")
#for i in error:
#	print(i)

rms=0
for i in range(len(error)):
	rms+=(error[i]**2)
rms=rms/len(error)
rms=rms**0.5

print(rms)
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
import numpy as np

b = int(input("Word size: "))     #Number of bits used to represent every Number 
e = int(input("Number of bits used to represent the exponent: "))       #Number of bits for exponent  
#The exponent is shown in biased representation
bias = pow(2,e-1)-1 

def ieee754_rep(a,b,e,bias):
    if(str(a)[0]=="-"):
        fp = "1"
    else:
        fp = "0"
    if(abs(a)==0):
        fp = fp + "0"*(b-1)
        return fp
        # elif(abs(a)==inf):
        #     fp = fp + "1"*e + "0"*(b-e-1)
        #Infinity can't be represented in Python and is not needed in the calculations either
    else:
        frac = float("0."+str(a)[str(a).index(".")+1:]) 
        a = bin(int(a))[2:]
        exp = len(a)
        n = b-e-1
        for k in range(n):
            frac = frac*2
            a = a + str(frac)[0]
            frac = float("0"+str(frac)[1:])
        exp = bias + exp-1-str(a).index("1")
        # print(exp)
        if(exp>pow(2,e)):
            print("error: Exponent exceeded limit")
            exit()
        a = str(a)[str(a).index("1")+1:]
        fp = fp + (e-len(bin(exp)[2:]))*"0" + bin(exp)[2:] + a[0:b-e-1]
        fp = fp + "0"*(b-len(fp))
        return fp

file_input = input("File to read the data from: ")
num = np.genfromtxt(file_input,dtype=float,delimiter=",")
n = np.size(num,0)
m = np.size(num,1)

file_fp = input("File to write the data: ")
fp_data = open(file_fp,'w')

fp = [["0" for j in range(m)] for i in range(n)]
for i in range(n):  
    for j in range(m):  
        fp[i][j] = ieee754_rep(num[i][j],b,e,bias)
        fp_data.write("%s," %fp[i][j])
    fp_data.write("\n")
fp_data.close()

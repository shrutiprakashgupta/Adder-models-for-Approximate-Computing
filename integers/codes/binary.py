import numpy as np

def twos_comp(a):
    #Twos complement of positive numbers shall be used to store negative vakues
    bits = len(bin(a)[2:])
    a = bin((1<<bits) - a)[2:]
    a = '1'+'0'*(bits-len(a))+a
    return a

def bin_rep(a):
    #Padding the sign bit at the beginning (0-positive, 1-negative) 
    if(a<0):
        bin_a = twos_comp(abs(a))
    else:
        bin_a = '0'+bin(a)[2:]
    return bin_a

#The csv file containing input values
file_in = input("Integer Data File: ")
num = np.genfromtxt(file_in,dtype=int,delimiter=",")

file_out = input("File to write binary data: ")
data = open(file_out,'w')
n = np.size(num,axis=0)
m = np.size(num,axis=1)
binary = [['0' for j in range(m)] for i in range(n)]
for i in range(n):  
    for j in range(m):  
        #Conversion into Binary 
        binary[i][j] = bin_rep(num[i,j])
        data.write("%s," %binary[i][j])
    data.write("\n")
data.close()
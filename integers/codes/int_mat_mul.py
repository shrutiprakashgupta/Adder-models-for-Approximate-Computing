import numpy as np 

def twos_comp(a):
    bits = len(a)
    a = bin((1<<bits) - int(a,2))[2:]
    return a

def add_approx(a, b, c):
    #Look up table for the inexact adder
    lookup = [['0','0'],['1','0'],['0','1'],['1','0'],['0','1'],['1','0'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def add_exact(a, b, c):
    lookup = [['0','0'],['1','0'],['1','0'],['0','1'],['1','0'],['0','1'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def adder(a, b):
    result = ''
    res = ['0','0']
    bin_a = ('0'*(max(len(a),len(b))-len(a)) + a)[::-1]
    bin_b = ('0'*(max(len(b),len(b))-len(b)) + b)[::-1]
    
    app = 0
    for i in range(app):
        res = add_approx(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
    for i in range(app,len(bin_a)):
        res = add_exact(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    result = result + res[1]
    result = result[len(result)::-1]
    return result

def multiplier(a, b):
    prd = ["0", 0]
    if(a[0]!=b[0]):
        prd[1] = 1
    if(a[0]=="1"):
        a = twos_comp(a)
    else:
        a = a[1:]
    if(b[0]=="1"):
        b = twos_comp(b)
    else:
        b = b[1:]
    i = 0
    for x in a[::-1]:
        if(x=='1'):
            partial = bin(int(b,2)<<i)[2:]
            prd[0] = adder(prd[0], partial)
        i = i+1
    return prd

def sign_add(a, b):
    
    bin_a = (a[0]*(max(len(a),len(b))-len(a)) + a)[::-1]
    bin_b = (b[0]*(max(len(a),len(b))-len(b)) + b)[::-1]
    result = ''
    res = ['0','0']
    
    #Set the number of bits computed with approximate adders
    app = 0
    if(app>len(a)):
        print("Limit exceeded the operand size.")
        exit()

    for i in range(app):
        res = add_approx(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    for i in range(app,len(bin_a)):
        res = add_exact(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    result = result[::-1]
    return result
    
file_in = input("Binary Data File 1: ")
file1 = open(file_in,'r')
n = int(input("No. of Rows: "))
content = file1.read()
a = [content.split(',\n')[i].split(',') for i in range(n)]
file1.close()

file_in = input("Binary Data File 2: ")
file2 = open(file_in,'r')
content = file2.read()
b = [content.split(',\n')[i].split(',') for i in range(n)]
file2.close()

file_out = input("File to write the output: ")
file3 = open(file_out,'w')

m = len(a[0])

if((len(b)!=n)|(len(b[0])!=m)):
    print("Metrix dimensions do not match")
    exit()

for i in range(n):
    for j in range(m):
        prd = "0"
        for k in range(m):
            #Each term is calculated separately and added in the final term which gives the final value at the position i,j
            term = multiplier(a[i][k],b[k][j])
            #Padding the sign bit here, for using signed adder as all the terms may not be positive only 
            if(term[1]==0):
                term[0] = '0'+bin(int(term[0],2))[2:]
            else:
                bits = len(term[0])
                term[0] = bin((1<<bits) - int(term[0],2))[2:]
                term[0] = '1'+'0'*(bits-len(term[0]))+term[0]
            #Signed addition module
            prd = sign_add(prd, term[0])
        #Result converted into integer value 
        if(prd[0]=="0"):
            val = int(prd[1:],2)
        else:
            val = int(prd[1:],2) - (1<<len(prd[1:])) 
        file3.write("%s," %str(val))
    file3.write("\n")
file3.close()
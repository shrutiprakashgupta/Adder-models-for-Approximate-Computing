import numpy as np 

def twos_comp(a):
    bits = len(a)
    a = bin((1<<bits) - int(a,2))[2:]
    return a

def add_approx(a, b, c):
    lookup = [['0','0'],['1','0'],['0','1'],['1','0'],['0','1'],['1','0'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def add_exact(a, b, c):
    lookup = [['0','0'],['1','0'],['1','0'],['0','1'],['1','0'],['0','1'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def adder(a, b):
    result = ''
    res = ['0','0']
    #Sign extension is not used as values passed are always positive (magnitude only)
    #Sign bit is dealt separately
    bin_a = ('0'*(max(len(a),len(b))-len(a)) + a)[::-1]
    bin_b = ('0'*(max(len(b),len(b))-len(b)) + b)[::-1]
    
    #Set the number of bits to be computed with approximate adders
    #For exact calculation, set app = 0
    app = 2
    if(app>len(bin_a)):
        print("No. of approximated bits exceeded limit.")
        exit()
    for i in range(app):
        res = add_approx(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
    for i in range(app,len(bin_a)):
        res = add_exact(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    result = result+res[1]
    result = result[len(result)::-1]
    return result

def multiplier(a, b):
    prd = ["0", 0]
    if(a[0]!=b[0]):
        #sign of the product decided by XOR on the signs of operand
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
    #The above block changes the number into magnitude only
    for x in a[::-1]:
        if(x=='1'):
            #Each partial product is calculated by shifting and then added
            partial = bin(int(b,2)<<i)[2:]
            prd[0] = adder(prd[0], partial)
        i = i+1
        #The value returned by the module has the magnitude and the sign separated 
    return prd

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

prd = [["0" for j in range(len(a[0]))] for i in range(n)]
for i in range(n):
    for j in range(len(a[0])):
        term = multiplier(a[i][j],b[i][j])
        #Product of the corresponding terms of the two matrices calculated 
        prd[i][j] = pow(-1,term[1])*int(term[0],2)
        file3.write("%s," %str(prd[i][j]))
    file3.write("\n")
file3.close()
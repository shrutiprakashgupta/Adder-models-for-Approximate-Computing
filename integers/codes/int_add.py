print("Menu to perform Binary addition")
file_in = input("Binary Data File 1: ")
data = open(file_in,'r')
content = data.read()
a = content.split(",\n")
#If the input file is created with binary.py, then no need to change the delimiters
n = len(a)
a = [a[i].split(",") for i in range(n)]
m = len(a[0])
data.close()

file_in = input("Binary Data File 2: ")
data = open(file_in,'r')
content = data.read()
b = content.split(",\n")
#If the input file is created with binary.py, then no need to change the delimiters
n2 = len(b)
b = [b[i].split(",") for i in range(n2)]
data.close()

if((n2!=n)|(len(b[0])!=m)):
    print("Data sets do not have compatible sizes.")
    exit()

def add_bit_exact(a, b, c):
    lookup = [['0','0'],['1','0'],['1','0'],['0','1'],['1','0'],['0','1'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def add_bit_approx(a, b, c):
    lookup = [['0','0'],['1','0'],['0','1'],['1','0'],['0','1'],['1','0'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def twos_comp(a):
    bits = len(a)
    a = (1<<bits) - int(a,2)
    return a

def adder(a, b):
    bin_a = (a[0]*(max(len(a),len(b))-len(a)) + a)[::-1]
    bin_b = (b[0]*(max(len(a),len(b))-len(b)) + b)[::-1]

    result = ''
    res = ['0','0']
    
    #Set the number of bits to be computed with approximate adders
    #For exact calculation, set app = 0
    app = 2
    if(app>len(a)):
        print("Limit exceeded the operand size.")
        exit()

    for i in range(app):
        res = add_bit_approx(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    for i in range(app,len(bin_a)):
        res = add_bit_exact(bin_a[i], bin_b[i], res[1])
        result = result+res[0]
        
    result = result+res[1]
    result = result[len(result)::-1]
    print("result = "+result)

    if(a[0]==b[0]):
        if(result[0]=='1'):
            res[0] = twos_comp(result)
            res[1] = 1
        else:
            res[0] = int(result[1:],2)
            res[1] = 0
    else:
        if(result[0]=='0'):
            res[0] = twos_comp(result[1:])
            res[1] = 1
        else:
            res[0] = int(result[1:],2)
            res[1] = 0
            
    res[0] = pow(-1,res[1])*res[0]
    return res[0]

#output written to the OUTPUT file (in integer format)
file_out = input("File to write output data: ")
data = open(file_out,'w')
for i in range(n):  
    for j in range(m):  
        #Adding the Binary data (corresponding elemnets)
        print(a[i][j])
        print(b[i][j])
        sum_ab = adder(a[i][j],b[i][j])
        data.write("%s," %str(sum_ab))
    data.write("\n")
data.close()
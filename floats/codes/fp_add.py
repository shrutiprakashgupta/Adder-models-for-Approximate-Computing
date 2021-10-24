def exp_cmp(a,b,e):
    if(int(a[1:e+1],2)<int(b[1:e+1],2)):
        #first operand must have the larger exponent
        a,b = b,a
    d = int(a[1:e+1],2) - int(b[1:e+1],2)
    #the 1 bit which was dropped earlier is now added: 
    val_a = a[0]+"1"+a[e+1:]
    val_b = b[0]+"0"*d+"1"+b[e+1:]
    val_b = val_b[:len(val_a)]
    #The operands with the adjusted mantissa have the same exponent (as the larger one)
    exp = int(a[1:e+1],2)
    return val_a,val_b,exp

def twos_comp(a):
    a = "0"+a
    bits = len(a)
    a = bin((1<<bits) - int(a,2))[2:]
    a = '0'*(bits-len(a))+a
    return a[len(a)-bits:]

def adder(a, b):
    result = ''
    res = ['0','0']
    a = a[::-1]
    b = b[::-1]
    
    #Fix the number of bits to be approximated
    app = 3
    for i in range(app):
        res = add_approx(a[i], b[i], res[1])
        result = result+res[0]
    for i in range(app,len(a)):
        res = add_exact(a[i], b[i], res[1])
        result = result+res[0]
        
    result = result+res[1]
    result = result[len(result)::-1]
    # print(result)

    if(a[-1]==b[-1]):
        res[1] = a[-1]
        if(result[0]=='1'):
            l = len(result[1:])
            res[0] = bin((1<<l) - int(result[1:],2))[2:]
            res[0] = "0"*(l-len(res[0])) + res[0]
        else:
            res[0] = result[1:]
    else: 
        if(result[1]=='1'):
            l = len(result[1:])
            res[0] = bin((1<<l) - int(result[1:],2))[2:]
            res[0] = "0"*(l-len(res[0])) + res[0]
            res[1] = "1"
        else:
            res[0] = result[1:]
            res[1] = "0"
    return res

def add_exact(a, b, c):
    #The lookup table can directly be changed to incorporate any adder 
    lookup = [['0','0'],['1','0'],['1','0'],['0','1'],['1','0'],['0','1'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def add_approx(a, b, c):
    #The lookup table can directly be changed to incorporate any adder 
    lookup = [['0','0'],['1','0'],['0','1'],['1','0'],['0','1'],['1','0'],['0','1'],['1','1']]
    return lookup[4*int(a)+2*int(b)+int(c)]

def fp2dec(a,b,e,bias):
    #Gives the decimal representation of the number with the given IEEE 754 rep:
    val = pow(-1,int(a[0],2)) * int("1"+a[e+1:],2) * pow(2,int(a[1:e+1],2)-bias-(b-e-1))
    print(val)
    return val

def add_fp(x,y,b,e):
    #Exponent comparison block: (it returns the mantissa arraged properly so that the corresponding exponents are equal and the firt bit shows the sign)
    x,y,exp = exp_cmp(x,y,e)

    #first bit shows the sign and accordingly the two's complement is calculated
    if(x[0]=="1"):
        x = twos_comp(x[1:])
    if(y[0]=="1"):
        y = twos_comp(y[1:])
    
    #The adder block (For the floats also, similar block is applied for addition and calculating 2's comp)
    res = adder(x,y)

    #The result is Normalized (The trailing zeros removed and exponent adjusted accordingly)
    exp = exp+1-res[0].index("1")
    res[0] = res[0][res[0].index("1")+1:] 
    res[0] = res[0] + "0"*(b-e-1-len(res[0]))
    result = res[1] + "0"*(e-len(bin(exp)[2:])) + bin(exp)[2:] + res[0][:b-e-1]
    #The result is put back into IEEE 754 rep
    return result
    
#Representation specific: 
b = int(input("Number of bits in each floating point: "))
e = int(input("Bits reserved for exponent: "))
bias = pow(2,e-1)-1

#Performs Matrix addition: (The given size of matrix is the number of rows: Number of Columns may vary)
n = int(input("No. of rows in input file: "))

#File_a gives the name of the file in which IEEE 754 reps are stored
file_a = input("File 1: ")
file1 = open(file_a,'r')
content = file1.read()
mat_a = [content.split(',\n')[i].split(',') for i in range(n)]
file1.close()
print(mat_a)

file_b = input("File 2: ")
file2 = open(file_b,'r')
content = file2.read()
mat_b = [content.split(',\n')[i].split(',') for i in range(n)]
file2.close()
print(mat_b)

#The file in which output is to be written:
fp_res = input("File output: ")
fp_add_res = open(fp_res,'w')

#The following matrix stores the decimal values calculated using IEEE 754 std and the given adder
added = [[0 for j in range(len(mat_a[0]))] for i in range(n)]

for i in range(n):
    for j in range(len(mat_a[0])):
        #To check the decimal rep - uncomment the following commands
        # fp2dec(mat_a[i][j],b,e,bias)
        # fp2dec(mat_b[i][j],b,e,bias)
        added_fp = add_fp(mat_a[i][j],mat_b[i][j],b,e)
        added[i][j] = fp2dec(added_fp,b,e,bias)
        fp_add_res.write("%s," %str(added[i][j]))    
    fp_add_res.write("\n")
fp_add_res.close()

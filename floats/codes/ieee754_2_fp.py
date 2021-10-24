#This module converts IEEE 754 representation of a number to the decimal form for easy comprehension
b = 32
e = 8
bias = pow(2,e-1) - 1
file_name = input("Name of the file: ")
n = int(input("Number of rows: "))
file_fp = open(file_name, "r")
fp = file_fp.read()
fp = [fp.split(",\n")[i].split(",") for i in range(n)]
file_fp.close()
file_name =input("File to write the values: ")
file_fp = open(file_name, "w")
val = [[0 for j in range(len(fp[0]))] for i in range(n)]
for i in range(n):
    for j in range(len(fp[0])):
        a = fp[i][j]
        val[i][j] = pow(-1,int(a[0],2)) * int("1"+a[e+1:],2) * pow(2,int(a[1:e+1],2)-bias-(b-e-1))
        file_fp.write("%s," %str(val[i][j]))
    file_fp.write("\n")
file_fp.close()

#Max: 680564693277057719623408366969033850880
#Min: (Absolute) 5.877471754111438e-39
#Min: -680564693277057719623408366969033850880
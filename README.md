# Introduction 
This repository provides Python modules to convert input given as signed decimal numbers (integers and floating points, both are supported) into standard notations i.e. 8 bit 2's complement representation for integers and IEEE 754 32 bit representation for floating point numbers. It then processes them  through the adder and multiplier blocks which can be exact and approximate based on the truth table incorporated. A simple change in code may transform the adder (which is the basic unit in both the processes) into any proposed design to be analyzed and the number of bits to be processed in exact and approximate mode can also be fixed. 
# Usability:
Such simulational tools are used widely in the field of approximate computing to monitor the extent of error generated to select or reject any proposed design for a specific application.<br/>In the image compression domain, most of the computations involved are matrix operations involving addition, subtraction and multiplication. All are supproted by these modules and so their combination may be used to implement any sub-block of the whole image compression architecture.   
# Requirements: 
You would need Python 3 compiler to execute the codes, however to change the adder truth tables any text editor will work. The input files are given in the text format as specified in the code. The input/output files given in the data folder may prove helpful in case of any confusion regarding the data format in the files. 
#Output: 
For easy comprehension of the users, the inputs and outputs are generated in the decimal format, while the whole processing is performed in binary numbers, decomposed at the bit level. The program itself manages the intermediate steps. 
# Goals:
- [x] Modeling approximate adders and multipliers for integers 
- [x] Modeling approximate adders and multipliers for floating point numbers using the IEEE 754 notation
- [ ] Generating a Verilog model of the adder and multiplier blocks with direct substitutional units for approximate designs

# Write a program to convert binary to decimal
def binaryToDecimal(testInput):
    # reversing a string to ensure the last element is in the position 2 power 0
    reversedInput = testInput[::-1]
    # initializing a variable to hold the final result
    decimalOutput = 0
    # using enumerate to count and iterate in the same step
    for count,digit in enumerate(reversedInput):
        # using the conversion algorithm
        decimalOutput = (int(digit)*pow(2,count)) + decimalOutput
    return decimalOutput

# Write a program to convert decimal to binary
def decimalToBinary(testInput):
    binaryOutput = ''
    while testInput > 0:
        binaryOutput = str(testInput % 2) + binaryOutput
        testInput = testInput // 2

    if binaryOutput == '':
        return 0
    else:
        return binaryOutput




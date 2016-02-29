sqrArray=[][]
sqrArray[0][0] = "00"
sqrArray[0][1] = "01"
sqrArray[0][2] = "02"
sqrArray[0][3] = "03"

sqrArray[1][0] = "10"
sqrArray[1][1] = "11"
sqrArray[1][2] = "12"
sqrArray[1][3] = "13"

sqrArray[2][0] = "20"
sqrArray[2][1] = "21"
sqrArray[2][2] = "22"
sqrArray[2][3] = "23"

sqrArray[3][0] = "30"
sqrArray[3][1] = "31"
sqrArray[3][2] = "32"
sqrArray[3][3] = "33"

def function(string):
    stringArray = []
    for i in string:
        stringArray.append(i)

    for j in range (int(len(string)/2), int(len(string))):
        if stringArray[j] == stringArray[int(len(string)) - j - 1]:
            continue
        else:
            return False
    return True

    # if len(string) % 2 == 0:
    #     a = int(len(string)/2)-1
    #     b = a+1
    # else:
    #     a = int(len(string)/2) - 1
    #     b = a + 2
    #
    # while (a > 0) or (b < len(string)-1):
    #     if stringArray[a] == stringArray[b]:
    #         a -= 1
    #         b += 1
    #     else:
    #         return False
    #
    # return True


def squareArraySwap(array):
    print (array)




squareArraySwap(sqrArray)
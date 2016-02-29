points = [[45, -99], [24, 83], [-48, -68], [-97, 99], \
[-8, -77], [-2, 50], [44, 41], [-48, -58], \
[-1, 53], [14, 86], [31, 94], [12, -91], \
[33, 50], [82, 72], [83, -90], [10, 78], \
[7, -22], [90, -88], [-21, 5], [6, 23]]


def main():
    shortest = float("inf")

    for i in range (0, len(points)):
        for j in range(i+1,len(points)):
            shortest = calculateDist(points[i], points[j], shortest)

    print (shortest)

def calculateDist(x, y, shortest):
        x1 = x[0]
        x2 = x[1]

        y1 = y[0]
        y2=  y[1]

        sudoku(x)

        distance = ((x1 - y1)**2 + (x2 - y2)**2)**0.5

        if (int(distance < shortest)):
            return distance
        else:
            return shortest

if __name__ == "__main__": main()
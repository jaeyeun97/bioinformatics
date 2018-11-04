import numpy as np

gap_penalty = -8


class Blosum50(object):
    def __init__(self):
        self.matrix = dict()
        with open('blosum50.txt', 'r') as f:
            # First line
            ref = f.readline().split()
            for line in f:
                items = line.split()
                self.matrix[items[0]] = dict()
                for i in range(1, len(items)):
                    self.matrix[items[0]][ref[i-1]] = int(items[i])

    def find(self, c, d):
        return self.matrix[c][d]


def main(s1, s2):
    blosum = Blosum50()
    matrix = np.zeros((len(s1)+1, len(s2)+1), dtype=np.int8)
    arrows = np.zeros((len(s1)+1, len(s2)+1), dtype=np.int8)
    # First Line
    for j in range(1, len(s2)+1):
        matrix[0][j] = matrix[0][j-1] + gap_penalty
        arrows[0][j] = 2
    # Rest
    for i in range(1, len(s1)+1):
        matrix[i][0] = matrix[i-1][0] + gap_penalty
        arrows[i][0] = 1
        for j in range(1, len(s2)+1):
            t1 = matrix[i-1][j] + gap_penalty # above
            t2 = matrix[i][j-1] + gap_penalty # left
            t3 = matrix[i-1][j-1]  + blosum.find(s1[i-1], s2[j-1])
            matrix[i][j] = np.amax((t1, t2, t3))
            arrows[i][j] = np.argmax((t1, t2, t3)) + 1
    # Trace
    pointer = np.array([len(s1), len(s2)])
    trace = list()
    while arrows[tuple(pointer)] != 0:
        direction = arrows[tuple(pointer)]
        trace.append(direction) 
        if direction == 1:
            pointer[0] = pointer[0] - 1 # move on s1 axis
        elif direction == 2:
            pointer[1] = pointer[1] - 1 # move on s2 axis
        elif direction == 3:
            pointer[0] = pointer[0] - 1
            pointer[1] = pointer[1] - 1  

    output1 = list()
    output2 = list()
    pointer = np.zeros(2, dtype=int)
    for direction in reversed(trace):
        if direction == 1:
            pointer[0] = pointer[0] + 1
            output1.append(s1[pointer[0]-1]) 
            output2.append('-')
        elif direction == 2:
            pointer[1] = pointer[1] + 1
            output1.append('-')
            output2.append(s2[pointer[1]-1])
        elif direction == 3:
            pointer[0] = pointer[0] + 1
            pointer[1] = pointer[1] + 1
            output1.append(s1[pointer[0]-1]) 
            output2.append(s2[pointer[1]-1])
    return "".join(output1), "".join(output2)


if __name__ == "__main__":
    output1, output2 = main("PAWHEAE", "HEAGAWGHEE")
    print(output1)
    print(output2)

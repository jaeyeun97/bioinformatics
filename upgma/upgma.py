def sanitise(i):
    if isinstance(i, int):
        return (i,)
    else:
        return i 


class Cluster(object):  
    def __init__(self, content=None, cluster1=None, cluster2=None, weight=None):
        self.left = cluster1
        self.right = cluster2
        if content is not None:
            self.content = (content,)
            self.weight = 0 
        else:
            self.content = cluster1.content + cluster2.content
            self.weight = weight

    def tree(self):
        childs = ""
        if self.left and self.right:
            childs = " (L{}, R{})".format(self.left.tree(), self.right.tree())
        return "{}<{}>{}".format(self.content, self.weight, childs)

class Distance(object):
    def __init__(self, l):
        self.executed = False
        self.distance = dict()
        self.clusters = dict()
        for r in range(len(l)):
            self.distance[(r,)] = dict()
            self.clusters[(r,)] = Cluster(r)
            for i in range(len(l[r])):
                self.distance[(r,)][(i,)] = l[r][i]

    def getDistance(self, i, j):
        return self.distance[i][j]
    
    # i, j are keys
    def merge(self, i, j): 
        dist = self.distance[i][j]
        new_key = i + j
        self.distance[new_key] = dict()
        for start, v in self.distance.items():
            first = v[i] * len(i)
            second = v[j] * len(j)
            v.pop(i)
            v.pop(j)
            new_d = (first + second)/(len(i) + len(j))
            self.distance[start][new_key] = new_d
            self.distance[new_key][start] = new_d
            self.distance[new_key][new_key] = 0
        self.distance.pop(i)
        self.distance.pop(j)

        self.clusters[new_key] = Cluster(None, self.clusters[i], self.clusters[j], dist / 2)
        self.clusters.pop(i)
        self.clusters.pop(j) 

    def findClosest(self):
        return min([((s, e), d) for s, v in self.distance.items() for e, d in v.items() if d != 0], key=lambda p: p[-1])

    def exec(self):
        if not self.executed:
            while len(self.clusters) != 1:
                (s,e), d = self.findClosest()
                self.merge(s, e)
            self.executed = True
        return list(self.clusters.values())[0]

## Quite literally the shittest code I've every written
if __name__ == "__main__": 
    matrix = [[0, 3, 4, 4, 4], 
              [3, 0, 4, 4, 4], 
              [4, 4, 0, 1, 2], 
              [4, 4, 1, 0, 2], 
              [4, 4, 2, 2, 0]]
    d = Distance(matrix)      
    root = d.exec()
    print(root.tree())

import numpy as np
import matplotlib.pyplot as plt

def random_rate(p):
    return np.random.rand() < p


class SEIR():
    def __init__(self):
        self.N = int(1000)
        self.p = 0.006
        self.w = 0.2
        self.b = 0.5
        self.u = 0.2
        self.t = 100
        self.link = []
        for i in range(self.N):
            self.link.append([])
        # 0 S  1 E  2 I  3 R
        self.category = np.array(np.zeros([self.N], dtype=int))
        self.category[np.random.randint(self.N)] = 2

    def generate_graph(self):
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if random_rate(self.p):
                    self.link[i].append(j)
                    self.link[j].append(i)

    def print_graph(self):
        # for list in self.link:
        #     print(list)

        mxdeg=0
        for i in range(self.N):
            mxdeg=max(mxdeg,self.link[i].__len__())
        mxdeg+=1

        deg=[0]*mxdeg
        for i in range(self.N):
            deg[self.link[i].__len__()]+=1
        for i in range(mxdeg):
            deg[i]/=1.0*self.N
        plt.plot(np.linspace(0,mxdeg-1,mxdeg),deg)
        plt.xlabel('degree')
        plt.ylabel('P')
        plt.title('The probability distribution of degree')
        plt.show()

    def time_advancing(self):
        probability = np.array(np.zeros([self.N], dtype=float))
        for i in range(self.N):
            if self.category[i] != 0:
                continue
            count = 0
            for u in self.link[i]:
                if self.category[u] == 2:
                    count += 1
            probability[i] = 1 - np.float_power(1 - self.w, count)
        for i in range(self.N):
            if self.category[i] == 0:
                if random_rate(probability[i]):
                    self.category[i] = 1
            elif self.category[i] == 1:
                p = np.random.rand()
                if p < self.b:
                    self.category[i] = 2
                elif p < self.b + self.u:
                    self.category[i] = 3
            elif self.category[i] == 2:
                if random_rate(self.u):
                    self.category[i] = 3

    def count_number(self):
        res=[0,0,0,0]
        for i in range(self.N):
            res[self.category[i]]+=1
        return res

    def running(self):
        result=np.matrix(np.zeros([4,self.t+1], dtype=int))
        for i in range(self.t+1):
            numbers=self.count_number()
            for j in range(4):
                result[j,i]=numbers[j]
            self.time_advancing()
        self.show_result(result)

    def show_result(self,result):
        plt.title('SEIR model result')
        plt.xlabel('time')
        plt.ylabel('person')
        x=np.linspace(0,self.t,self.t+1)
        s1='SEIR'
        s2='>v<^'
        for idx in range(4):
            y=[]
            for i in range(self.t+1):
                y.append(result[idx,i])
            plt.plot(x,y,'-{}'.format(s2[idx]),label=s1[idx])
        plt.legend()
        plt.show()

model = SEIR()
model.generate_graph()
model.print_graph()
model.running()


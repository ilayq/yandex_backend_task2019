class Buffer:
    def __init__(self):
        self.arr = []

    def add(self, *vals):
        for i in range(len(vals)):
            self.arr.append(vals[i])
            if len(self.arr) == 5:
                print(sum(self.arr))
                self.arr = []

    def get_current_part(self):
        return self.arr

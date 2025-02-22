class BStopByAcc:
    def __init__(self, rounds, delta=0.01):
        '''
        连续rounds次, val_acc - max_val_acc > delta, 则停止训练
        '''
        self.rounds = rounds
        self.delta = delta
        self.max_val_acc = 0
        self.cnt = 0
    def __call__(self, val_acc):
        if val_acc <= self.max_val_acc - self.delta:
            self.cnt += 1
        if val_acc > self.max_val_acc:
            self.max_val_acc = val_acc
            self.cnt = 0
        if self.cnt > self.rounds:
            return True
        return False
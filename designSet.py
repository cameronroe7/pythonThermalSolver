# -*- coding: utf-8 -*-
class DesignSet():
    def __init__(self,mu = None):
        if mu is None:
            self.mu = (.4, .6, .8, 1.2, .1)
        else:
            self.mu = mu
        self.k = [1, *self.mu]
        self.Bi = self.mu[-1]
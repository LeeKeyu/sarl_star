#!/usr/bin/python

class Kalman:
	def __init__(self, Q=.002, R=1.0, P=.01):
		self.x = None
		self.Q = Q
		self.R = R
		self.P = P
		self.p = None

	def update(self, values):
		N = len(values)
		if self.x is None:
			self.x = values
			self.p = [self.P]*N
		else:
			for i in range(N):
				self.p[i] += self.Q
				k = self.p[i] / (self.p[i] + self.R)
				self.x[i] += k * (values[i] - self.x[i])
				self.p[i] = (1 - k) * self.p[i]

	def values(self):
		return self.x


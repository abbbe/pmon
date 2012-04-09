import matplotlib.pyplot as pyplot

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from PPPParam import PPPParam
from ProbeResCollector import ProbeResCollector

class ResGraph:
	'''
	Graph aggregating info for all probes
	'''
	def __init__(self, probes, ppp_params):
		self.ppp_params = ppp_params

		self.fig = pyplot.figure()

		## create a rescollector for each probe.
		## rescollectors creates subplots in

		self.rcs = {}
		
		nprobes = len(probes)
		for i in range(nprobes):
			probe = probes[i]
			rc = ProbeResCollector(self.fig, nprobes, i, self.ppp_params)
			self.rcs[probe] = rc

		self.fig.show()

	def add_result(self, probe, res):
		for _probe, rc in self.rcs.items():
			if _probe is probe:
				rc.add_result(res)

	def redraw(self):
		for _probe, rc in self.rcs.items():
			rc.redraw()

		self.fig.canvas.draw()

	def show(self):
		pyplot.show()


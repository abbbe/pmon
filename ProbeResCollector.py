import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from PPP import PPP

class ProbeResCollector:
	'''
	There is an instance of ProbeResCollector for each Probe instance.
	It keeps several instancess of PPP, for various time scales
	'''

	def __init__(self, fig, nrows, i, ppp_params):
		self.ppps = []

		for j in range(len(ppp_params)):
			ppp_param = ppp_params[j]
			n = i * len(ppp_params) + j + 1

			g = fig.add_subplot(nrows, len(ppp_params), n)

			ppp = PPP(ppp_param, g)
			self.ppps.append(ppp)

	def add_result(self, res):
		for ppp in self.ppps:
			ppp.add_result(res)

	def redraw(self):
		for ppp in self.ppps:
			ppp.redraw()


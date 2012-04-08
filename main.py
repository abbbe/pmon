from threading import Timer
from subprocess import check_output, CalledProcessError
import time, string
import matplotlib.pyplot as pyplot
import gtk, gobject

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from base import Base
from Probe import Probe, ProbeResult
from PPP import PPP
from PPPParam import PPPParam

class ResGraph:
	'''
	Graph aggregating info for all probes
	'''
	def __init__(self, probes):
		self.ppp_params = [PPPParam(5), PPPParam(60), PPPParam(600), PPPParam()]

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

		Timer(0.1, self.redraw).start()

	def add_result(self, probe, res):
		for _probe, rc in self.rcs.items():
			if _probe is probe:
				rc.add_result(res)

	def redraw(self):
		for _probe, rc in self.rcs.items():
			rc.redraw()

		self.fig.canvas.draw()

		Timer(0.1, self.redraw).start()

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

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

class ProbeSet:
	def __init__(self, probes, res_graph):
		self.probes = probes
		self.res_graph = res_graph

		Timer(0.1, self.run).start()

	def run(self):
		for probe in self.probes:
			logger.debug("//     start of running probe")
			res = self.run_probe(probe)
			logger.debug("||     before adding result")
			self.res_graph.add_result(probe, res)
			logger.debug("\\	end of running probe")
		logger.debug("// before commit")
		session.commit()
		logger.debug("\\\\ after commit")

		Timer(0.1, self.run).start()

        def run_probe(self, probe):
                start_time = time.time()
                try:
			logger.debug("* before calling")
                        output = check_output(probe.command, shell=True)
			logger.debug("* after calling")
                        return_code = 0
                except CalledProcessError:
			logger.debug("* got exception while calling")
                        return_code = -1

                end_time = time.time()

		dt = end_time - start_time

		logger.debug("* before creating ProbeResult()")
                res = ProbeResult(probe, start_time, end_time, return_code)
		logger.debug("* after creating ProbeResult()")

                return res

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///foo.db')
logger.debug("Running on sqlachemy version %s" % (sqlalchemy.__version__))

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine) 
logger.debug("Probe table: " + str(Probe.__table__))
logger.debug("ProbeResult table: " + str(ProbeResult.__table__))
logger.debug("SQLAlchemy initialized")

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

probe1 = Probe('ping', "ping -c 1 localhost")
probe2 = Probe('curl', "curl -s http://localhost/")
probes = [probe1, probe2]

for probe in probes:
	session.add(probe)
session.commit()

res_graph = ResGraph(probes)
probe_set = ProbeSet(probes, res_graph)

pyplot.show()

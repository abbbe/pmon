from subprocess import check_output, CalledProcessError
from threading import Timer
from Probe import ProbeResult
import time

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class ProbeController:
	'''
	This class is responsible for polling probes periodically, updating the graph, saving the results
	'''

	probe_poll_period = 1

	def __init__(self, probes, res_graph, data_store):
		self.probes = probes
		self.res_graph = res_graph
		self.data_store = data_store

	def start(self):
		logger.debug("start(), the first run scheduled in %fs" % (self.probe_poll_period))
		Timer(self.probe_poll_period, self.run).start()

	def run(self):
		logger.debug("// run() started")
		for probe in self.probes:
			logger.debug("//     start of running probe")
			res = self.run_probe(probe)
			logger.debug("||     before adding result")
			self.res_graph.add_result(probe, res)
			logger.debug("\\	end of running probe")
			self.data_store.add(res)
		logger.debug("// before commit")
		self.data_store.commit()
		logger.debug("\\\\ after commit")

		self.res_graph.redraw()

		Timer(self.probe_poll_period, self.run).start()
		logger.debug("\\\\ run() ended, rerun scheduled in %fs" % (self.probe_poll_period))

        def run_probe(self, probe):
                start_time = time.time()
                try:
			logger.debug("* before calling probe command '%s'" % (probe.command))
                        output = check_output(probe.command, shell=True)
			logger.debug("* after calling probe command")
                        return_code = 0
                except CalledProcessError:
			logger.debug("* got exception while calling probe command")
                        return_code = -1

                end_time = time.time()

		dt = end_time - start_time

		logger.debug("* before creating ProbeResult()")
                res = ProbeResult(probe, start_time, end_time, return_code)
		logger.debug("* after creating ProbeResult()")

                return res

#!/usr/bin/python

'''
This tool runs specified set of commands in a loop, measures the time it takes
to execute a command, captures its exit code. These results are stored in the
database and displayed on the graphs at different scales.
'''

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from Probe import Probe
from PPPParam import PPPParam

from ResGraph import ResGraph
from ProbeController import ProbeController
from DataStore import DataStore

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

data_store = DataStore()

probe1 = Probe('ping', "ping -c 1 localhost")
probe2 = Probe('curl', "curl -s http://localhost/")
probes = [probe1, probe2]

ppp_params = [PPPParam(60), PPPParam(900), PPPParam()]

for probe in probes:
	data_store.add(probe)
data_store.commit()

res_graph = ResGraph(probes, ppp_params)
probe_controller = ProbeController(probes, res_graph, data_store)
probe_controller.start()

res_graph.show()

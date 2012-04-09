import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from collections import deque
from threading import Lock

class PPP:
	def __init__(self, params, graph):
		self.period = params.period
		self.graph = graph

		logger.debug("Created PPP period %s" % (str(self.period)))

		self.ress = deque()
		self.tss = deque()
		self.errs = deque()
		self.dts = deque()

		self.wlock = Lock()

	def set_graph(self, graph):
		self.graph = graph

	def redraw(self):
		self.wlock.acquire()

		self.graph.clear()
		args = [self.tss, self.errs, 'ro-', self.tss, self.dts, 'b-']
		self.graph.plot(*args)

		self.wlock.release()

	def add_result(self, res):
		self.wlock.acquire()

                self.ress.append(res)
                self.tss.append(res.ts)
                self.errs.append(res.exit_code)
                self.dts.append(res.get_dt())

		if not self.period == None:
			# prune if there are more than two data points
			while len(self.ress) > 2:
				dt = res.ts - self.ress[0].ts
				logger.debug("> nress=%d, res.ts=%f, ress[0].ts=%f, dt=%f, period=%s"
					% (len(self.ress), res.ts, self.ress[0].ts, dt, str(self.period)))

				if dt <= self.period:
					# enough pruning
					break

				self.ress.popleft()
				self.tss.popleft()
				self.errs.popleft()
				self.dts.popleft()

		self.wlock.release()


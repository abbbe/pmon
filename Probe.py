from sqlalchemy import *
from sqlalchemy.orm import relationship

from base import Base

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Probe(Base):
        __tablename__ = 'probe'

        id = Column(Integer, Sequence('probe_id_seq'), primary_key=True)
	results = relationship("ProbeResult", backref="Probe.id")

        name = Column(String)
        command = Column(String)

        def __init__(self, name, command):
                self.name = name
                self.command = command

        def __repr__(self):
                return "<Probe('%s', '%s')>" % (self.name, self.command)

class ProbeResult(Base):
        __tablename__ = 'probe_result'

        id = Column(Integer, Sequence('probe_result_id_seq'), primary_key=True)
        probe_id = Column(Integer, ForeignKey('probe.id'))

        ts = Column(Integer)
        end_ts = Column(Integer)
        exit_code = Column(Integer)

        def __init__(self, probe, ts, end_ts, exit_code):
		logger.debug("in ProbeResult::__init__(probe.id=%d)" % (probe.id))
                self.probe_id = probe.id
                self.ts = ts
                self.end_ts = end_ts
                self.exit_code = exit_code

	def get_dt(self):
		return self.end_ts - self.ts

        def __repr__(self):
                return "<ProbeResult(%s, %s, %s, %s)>" % (str(self.probe_id), self.ts, self.end_ts, self.exit_code)


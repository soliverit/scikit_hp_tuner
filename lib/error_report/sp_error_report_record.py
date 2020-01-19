from .error_report_record_base import ErrorReportRecordBase
class SPErrorReportRecord(ErrorReportRecordBase):
	def __init__(self, inputs, x, y, sx, sy):
		super().__init__(inputs, x, y)
		self.sx 	= sx
		self.sy		= sy
		self.sDelta	= sx - sy
		self.sAbsDelta	= abs(sx) + abs(sy)
		self.sse	= self.sDelta ** 2
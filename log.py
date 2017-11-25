import datetime
import threading
try:
	import thread
except:
	pass
from enum import Enum


class ELevel(Enum):
	debug = 1
	verbose = 2
	info = 3
	notice = 4
	warning = 5
	error = 6

def get_thread_ident():
	try:
		thread_ident = thread.get_ident()
	except:
		thread_ident = threading.get_ident()
	return thread_ident


class LoggerBackendConsole:
	def log(self, time, level, ndc_list, message):
		time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')
		time_str = time_str[0:-3]
		time_str = time_str + 'Z'
		max_level_str_length = 7
		level_str = level.name.ljust(max_level_str_length)
		attention_str = ' '
		if level.value >= ELevel.notice.value:
			attention_str = '!'
		ndc_str = '/'.join(ndc_list)
		ndc_str = '/' + ndc_str
		s = '{} {}{} {}  {}'.format(
			time_str,
			attention_str,
			level_str,
			ndc_str,
			message
		)
		print(s)


class Lock:
	def __init__(self, mutex):
		self.mutex = mutex 

	def __enter__(self):
		self.mutex.acquire()

	def __exit__(self, type, value, traceback):
		self.mutex.release()


class Logger:
	def __init__(self, backend_list):
		self.backend_list = backend_list
		self.next_thread_id = 0
		self.thread_ident_to_id = dict()
		self.thread_id_to_ndc_list = dict()
		self.mutex = threading.Lock()

	def _get_thread_id(self):
		thread_ident = get_thread_ident()
		thread_id = self.thread_ident_to_id.get(thread_ident)
		if thread_id is None:
			thread_id = str(self.next_thread_id)
			self.next_thread_id += 1
			self.thread_ident_to_id[thread_ident] = thread_id
		return thread_id

	def _get_ndc_list(self):
		thread_id = self._get_thread_id()
		ndc_list = self.thread_id_to_ndc_list.get(thread_id)
		if not ndc_list:
			ndc_list = [thread_id]
			self.thread_id_to_ndc_list[thread_id] = ndc_list
		return ndc_list

	def log(self, level, message):
		with Lock(self.mutex):
			now_datetime = datetime.datetime.utcnow()
			ndc_list = self._get_ndc_list()
			for backend in self.backend_list:
				backend.log(now_datetime, level, ndc_list, message)


	def ndc_push(self, ndc_name):
		with Lock(self.mutex):
			ndc_list = self._get_ndc_list()
			ndc_list.append(ndc_name)

	def ndc_pop(self):
		with Lock(self.mutex):
			ndc_list = self._get_ndc_list()
			ndc_list.pop()


def get_logger():
	if not get_logger.instance:
		backend = LoggerBackendConsole()
		backend_list = [backend]
		get_logger.instance = Logger(backend_list)
	return get_logger.instance
get_logger.instance = None


def log(level, message):
	logger = get_logger()
	logger.log(level, message)


def debug(message):
	log(ELevel.debug, message)

def verbose(message):
	log(ELevel.verbose, message)

def info(message):
	log(ELevel.info, message)

def notice(message):
	log(ELevel.notice, message)

def warning(message):
	log(ELevel.warning, message)

def error(message):
	log(ELevel.error, message)


class Nest:
	def __init__(self, ndc_name):
		self.ndc_name = ndc_name

	def __enter__(self):
		self.start_datetime = datetime.datetime.utcnow()
		logger = get_logger()
		logger.ndc_push(self.ndc_name)
		info('{')

	def __exit__(self, type, value, traceback):
		end_datetime = datetime.datetime.utcnow()
		duration = end_datetime - self.start_datetime
		info('}} {}'.format(duration))
		logger = get_logger()
		logger.ndc_pop()


class NestDeco:
	def __call__(self, func):
		def my_logic(*args, **kwargs):
			with Nest(func.__name__):
				result = func(*args, **kwargs)
				return result
		return my_logic


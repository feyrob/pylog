import log

@log.NestDeco()
def test_planet():
	log.verbose('probe initialization')
	with log.Nest('measuring'):
		log.info('stickyness okay')
		log.notice('foggy ground')
	log.warning('exact measurements not possible')

def example():
	log.debug('double good habitat evaluator 2.0')
	test_planet()
	log.error('habitat not suitable')

if __name__ == '__main__':
	example()

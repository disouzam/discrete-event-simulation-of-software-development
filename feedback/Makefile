all: \
  analyze_simple_testing_queues_1000.svg \
  analyze_simple_testing_times_1000.svg

analyze_simple_testing_queues_1000.svg analyze_simple_testing_times_1000.svg: analyze_simple_testing.py simple_testing.py
	python $(word 2, $^) | python $< analyze_simple_testing_queues_1000.svg analyze_simple_testing_times_1000.svg

clean:
	@rm -f *~ *.svg

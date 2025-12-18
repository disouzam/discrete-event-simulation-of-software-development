all: \
  analyze_simple_testing_queues.svg \
  analyze_simple_testing_times.svg \
  analyze_same_testing.svg

analyze_simple_testing_queues.svg analyze_simple_testing_times.svg: analyze_simple_testing.py simple_testing.py
	python $(word 2, $^) | python $< analyze_simple_testing_queues.svg analyze_simple_testing_times.svg

analyze_same_testing.svg: analyze_same_testing.py same_testing.py
	python $(word 2, $^) | python $< $@

clean:
	@rm -f *~ *.svg

all: \
  fixed_work_and_break.out \
  uniform_work_and_break.out \
  visualize_uniform_work_and_break.svg \
  manager_developer_queue.json

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

visualize_uniform_work_and_break.svg: visualize_start_stop_json.py monitor_uniform_work_and_break.json
	cat $(word 2, $^) | python $< $@

clean:
	@rm -f *~ *.json *.out *.svg

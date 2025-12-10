all: \
  fixed_work_and_break.out \
  uniform_work_and_break.out \
  monitor_uniform_work_and_break.json \
  plot_log_normal.svg \
  visualize_uniform_work_and_break.svg

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

plot_log_normal.svg: plot_log_normal.py
	python $< $@

visualize_uniform_work_and_break.svg: visualize_uniform_work_and_break.py monitor_uniform_work_and_break.json
	cat $(word 2, $^) | python $< $@

all: \
  fixed_work_and_break.out \
  plot_log_normal.svg

%.out: %.py
	python $< >& $@

%.svg: %.py
	python $< $@

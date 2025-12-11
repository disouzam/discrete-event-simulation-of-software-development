all: \
  plot_exponential.svg \
  plot_log_normal.svg \
  multiple_programmers.json

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

plot_%.svg: plot_%.py
	python $< $@

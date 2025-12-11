all: \
  m1_d1_fixed.out \
  plot_exponential.svg \
  plot_log_normal.svg

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

plot_%.svg: plot_%.py
	python $< $@

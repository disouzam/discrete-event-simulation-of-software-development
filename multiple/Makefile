all: \
  m1_d1_fixed.out

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

plot_log_normal.svg: plot_log_normal.py
	python $< $@

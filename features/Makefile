all: \
  analyze_strict_priorities.svg

%.out: %.py
	python $< >& $@

%.json: %.py
	python $< >& $@

analyze_strict_priorities.svg: analyze_strict_priorities.py strict_priorities.py
	python $(word 2, $^) | python $< $@

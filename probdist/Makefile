TARGETS = \
  uniform_interaction.txt \
  uniform_interaction_coder.txt \
  uniform_interaction_manager.txt \
  random_interaction.txt \
  random_interaction_coder.txt \
  random_interaction_manager.txt \
  exponential.svg \
  lognormal.svg \

all: ${TARGETS}

%.txt: %.py
	python $< > $@

uniform_interaction_coder.txt: uniform_interaction.txt
	grep coder $< > $@

uniform_interaction_manager.txt: uniform_interaction.txt
	grep manager $< > $@

random_interaction_coder.txt: random_interaction.txt
	grep coder $< > $@

random_interaction_manager.txt: random_interaction.txt
	grep manager $< > $@

%.svg: %.py
	python $< $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

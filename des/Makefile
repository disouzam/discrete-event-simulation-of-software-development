TARGETS = \
  ask_for_work.txt \
  simple_interaction.txt \
  simple_interaction_coder.txt \
  simple_interaction_manager.txt \

all: ${TARGETS}

%.txt: %.py
	python $< > $@

simple_interaction_coder.txt: simple_interaction.txt
	grep coder $< > $@

simple_interaction_manager.txt: simple_interaction.txt
	grep manager $< > $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

TARGETS = \
  ask_for_work.txt \
  simple_interaction.txt \
  simple_interaction_coder.txt \
  simple_interaction_manager.txt \
  simple_interaction_marimo_alternative_output.txt \
  simple_interaction_marimo_alternative_output_2.txt

all: ${TARGETS}

%.txt: %.py
	python $< > $@

simple_interaction_coder.txt: simple_interaction.txt
	grep coder $< > $@

simple_interaction_manager.txt: simple_interaction.txt
	grep manager $< > $@

simple_interaction_marimo_alternative_output_2.txt: simple_interaction_marimo_alternative_output.txt
	bash sanitize-colorized-output.sh $< $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

TARGETS = \
  ask_for_work.txt \
  simple_interaction.txt \
  simple_interaction_coder.txt \
  simple_interaction_manager.txt \
  introduce_structure_json.json \
  introduce_structure_df.txt

all: ${TARGETS}

%.txt: %.py
	python $< > $@

simple_interaction_coder.txt: simple_interaction.txt
	grep coder $< > $@

simple_interaction_manager.txt: simple_interaction.txt
	grep manager $< > $@

uniform_interaction_coder.txt: uniform_interaction.txt
	grep coder $< > $@

uniform_interaction_manager.txt: uniform_interaction.txt
	grep manager $< > $@

random_interaction_coder.txt: random_interaction.txt
	grep coder $< > $@

random_interaction_manager.txt: random_interaction.txt
	grep manager $< > $@

introduce_structure_json.json: introduce_structure_json.sh introduce_structure.py
	bash $< > $@

introduce_structure_df.txt: introduce_structure_df.sh introduce_structure.py
	bash $< > $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

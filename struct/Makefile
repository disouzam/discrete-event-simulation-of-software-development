TARGETS = \
  introduce_structure_json.json \
  introduce_structure_df.txt

all: ${TARGETS}

%.txt: %.py
	python $< > $@

introduce_structure_json.json: introduce_structure_json.sh introduce_structure.py
	bash $< > $@

introduce_structure_df.txt: introduce_structure_df.sh introduce_structure.py
	bash $< > $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

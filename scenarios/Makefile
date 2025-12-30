JOB_PRIORITY = \
  job_priority_ages.svg \
  job_priority_backlog.svg \
  job_priority.txt

REWORK = \
  rework_same.svg

SMOOTHING = \
  smoothing_ages_1.svg \
  smoothing_ages_10.svg \
  smoothing_ages_100.svg \
  smoothing_ages_1000.svg

TARGETS = \
  ${JOB_PRIORITY} \
  ${SMOOTHING} \
  ${REWORK}

all: ${TARGETS}

${JOB_PRIORITY}: job_priority.py
	python $< \
	--figure job_priority_ages.svg job_priority_backlog.svg \
	--table \
	policy=oldest,newest,shortest,longest t_sim=1000 \
	> job_priority.txt

${SMOOTHING}: smoothing.py
	python smoothing.py --figure smoothing_ages_1.svg -- n_iter=1
	python smoothing.py --figure smoothing_ages_10.svg -- n_iter=10
	python smoothing.py --figure smoothing_ages_100.svg -- n_iter=100
	python smoothing.py --figure smoothing_ages_1000.svg -- n_iter=1000

rework_same.svg: rework_same.py make_state_graph.py
	python rework_same.py t_sim=400 \
	| python make_state_graph.py \
	| dot -Tsvg \
	> $@

clean:
	@rm -rf *~ __pycache__

sterile: clean
	@rm -f ${TARGETS}

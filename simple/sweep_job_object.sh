for t in 100 1000 10000 100000
do
    echo $t
    python job_object.py 12345 $t | python analyze_job_object.py
done

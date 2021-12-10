#!/bin/sh
CONVERGE=1
ITER=1
rm v v1 log*

$HADOOP_HOME/bin/hadoop dfsadmin -safemode leave
hdfs dfs -rm -r /Big_Data_Assignments/Assignment-2/output 

hadoop jar $HADOOP_HOME/hadoop-streaming-3.2.2.jar \
-mapper "'/home/pes1ug19cs019/Desktop/Assignment2/mapper_t1.py'" \
-reducer "'/home/pes1ug19cs019/Desktop/Assignment2/reducer_t1.py' '/home/pes1ug19cs019/Desktop/Assignment2/v'" \
-input /Big_Data_Assignments/Assignment-2/INPUT/dataset_1percent.txt \
-output /Big_Data_Assignments/Assignment-2/output/task-1-output

while [ "$CONVERGE" -ne 0 ]
do
	echo "############################# ITERATION $ITER #############################"
	hadoop jar $HADOOP_HOME/hadoop-streaming-3.2.2.jar \
	-mapper "'/home/pes1ug19cs019/Desktop/Assignment2/mapper_t2.py' '/home/pes1ug19cs019/Desktop/Assignment2/v' '/home/pes1ug19cs019/Desktop/Assignment2/embedding_1percent.json'" \
	-reducer "'/home/pes1ug19cs019/Desktop/Assignment2/reducer_t2.py'" \
	-input /Big_Data_Assignments/Assignment-2/output/task-1-output/part-00000 \
	-output /Big_Data_Assignments/Assignment-2/output/task-2-output/
	touch v1
	hadoop dfs -cat /Big_Data_Assignments/Assignment-2/output/task-2-output/part-00000 > "/home/pes1ug19cs019/Desktop/Assignment2/v1"
	CONVERGE=0 #$(python3 check_conv.py $ITER>&1)
	ITER=$((ITER+1))
	hdfs dfs -rm -r /Big_Data_Assignments/Assignment-2/output/task-2-output/
	echo $CONVERGE
done

from pyspark.sql import SparkSession as spark
import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext

spark_context = SparkContext.getOrCreate()
sql_context = SQLContext(spark_context)

country = sys.argv[1]
df_path = sys.argv[2]
df = sql_context.read.csv(df_path, header=True)

df = df.filter(df.Country == country)
df = df.withColumn("AverageTemperature", df.AverageTemperature.cast("float"))
df_grouped = df.groupBy("City").avg("AverageTemperature")

df_grouped = df_grouped.withColumnRenamed("avg(AverageTemperature)", "avg_temp")
df_grouped = df_grouped.withColumnRenamed("City", "city_name")

df_joined = df.join(df_grouped, df.City == df_grouped.city_name)
df_final = df_joined.filter(df_joined.AverageTemperature > df_joined.avg_temp)

df_final = df_final.groupBy("City").count()
df_final = df_final.sort("City")

final_list = df_final.select("City", "count").rdd.map(lambda x: (x[0], x[1])).collect()

for line in final_list:
    print("%s\t%s" % (line[0],line[1]))

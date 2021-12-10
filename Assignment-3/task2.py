from pyspark.sql import SparkSession as spark
import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext

spark_context = SparkContext.getOrCreate()
sql_context = SQLContext(spark_context)

df_path = sys.argv[1]
df1_path = sys.argv[2]

# df = spark.read.csv("city_sample_5percent.csv", header=True)
# df1 = spark.read.csv("global.csv", header=True)

df = sql_context.read.csv(df_path, header=True)
df1 = sql_context.read.csv(df1_path, header=True)

df1 = df1.withColumnRenamed("dt", "date")
df = df.filter(df.AverageTemperature.isNotNull())
df = df.filter(df.dt.isNotNull())
df = df.filter(df.City.isNotNull())
df = df.filter(df.Country.isNotNull())

df1 = df1.filter(df1.LandAverageTemperature.isNotNull())
df1 = df1.filter(df1.date.isNotNull())


df = df.withColumn("AverageTemperature", df.AverageTemperature.cast("float"))
df1 = df1.withColumn("LandAverageTemperature", df1.LandAverageTemperature.cast("float"))
df = df.withColumn("dt", df.dt.cast("date"))
df1 = df1.withColumn("date", df1.date.cast("date"))


df = df.groupBy("dt", "Country").agg({"AverageTemperature": "max"})
df_joined = df.join(df1, df.dt == df1.date)

df_joined = df_joined.withColumnRenamed("max(AverageTemperature)", "maxTemp")

df_joined = df_joined.filter(df_joined.maxTemp > df_joined.LandAverageTemperature)
df_final = df_joined.groupBy("Country").count()
df_final = df_final.sort("Country")

final_list = df_final.select("Country", "count").rdd.map(lambda x: (x[0], x[1])).collect()

for line in final_list:
    print("%s\t%s" % (line[0],line[1]))




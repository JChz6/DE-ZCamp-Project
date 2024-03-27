from pyspark.sql import SparkSession

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--date', required=True)
args = parser.parse_args()
date = args.date


# Create SparkSession from builder
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local") \
                    .appName('project-pipeline') \
                    .getOrCreate()

df = spark.read.csv(f'gs://peru-real-state-datalake/{date}/*.csv', header=True, inferSchema=True, multiLine=True)

from pyspark.sql.functions import when
from pyspark.sql.functions import expr
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import FloatType, IntegerType
from pyspark.sql.functions import col, substring, row_number
from pyspark.sql.window import Window

#Normalize some values in "property_type"
df = df.withColumn("property_type", when(df["property_type"] == "casas", "house").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "departamentos", "apartment").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "oficinas", "office").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "casas-playa", "beach house").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "locales-comerciales", "store").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "casas-condominio", "house").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "terrenos", "land").otherwise(df["property_type"]))
df = df.withColumn("property_type", when(df["property_type"] == "residenciales", "residential").otherwise(df["property_type"]))
df = df.withColumn("operation", when(df["operation"] == "venta", "sale").otherwise(df["operation"]))
df = df.withColumn("operation", when(df["operation"] == "alquiler", "rents").otherwise(df["operation"]))

#Clean the values in "price" column and convert them to float
clean = df.withColumn('price', regexp_replace('price', '\n', ''))
clean = clean.withColumn('price', regexp_replace('price', ' ', ''))
clean = clean.withColumn('price', regexp_replace('price', '\\$', ''))
clean = clean.withColumn('price', regexp_replace('price', ',', ''))
clean = clean.withColumn("price", clean["price"].cast(FloatType()))

#Clean the values in "size_m2" and convert them to float
clean = clean.withColumn("size_m2", regexp_replace("size_m2", "m2", ""))
clean = clean.withColumn("size_m2", clean["size_m2"].cast(FloatType()))


clean = clean.withColumn("description", regexp_replace("description", '"', ""))
clean = clean.withColumn("name", regexp_replace("name", '"', ""))
clean = clean.withColumn("specs", regexp_replace("specs", '"', ""))
clean = clean.withColumn("url", regexp_replace("url", '"', ""))

clean = clean.withColumn("description", regexp_replace("description", ',', ";"))
clean = clean.withColumn("name", regexp_replace("name", ',', ";"))
clean = clean.withColumn("specs", regexp_replace("specs", ',', ";"))
clean = clean.withColumn("url", regexp_replace("url", ',', ";"))


#Clean some irregular values in "city"
clean = clean.withColumn("city", regexp_replace("city", "-departamento/list", ""))

#Convert the coordinates to float
clean = clean.withColumn("longitude_x", clean["longitude_x"].cast(FloatType()))
clean = clean.withColumn("latitude_y", clean["latitude_y"].cast(FloatType()))

#Delete the strings from "rooms" and "bathrooms" and convert them to integer
clean = clean.withColumn("rooms", regexp_replace("rooms", " Habitaciones", ""))
clean = clean.withColumn("bathrooms", regexp_replace("bathrooms", " Baños", ""))
clean = clean.withColumn("rooms", clean["rooms"].cast(IntegerType()))
clean = clean.withColumn("bathrooms", clean["bathrooms"].cast(IntegerType()))

#Clean the empty spaces and the unnecesary characters in "specs"
clean = clean.withColumn('specs', regexp_replace('specs', '\n', ''))
clean = clean.withColumn('specs', regexp_replace('specs', '\\s{2,}', ' '))
clean = clean.withColumn('specs', substring(col('specs'), 2, 1000000))

#Delete the "https://www." from the urls
clean = clean.withColumn('url', regexp_replace("url", "https://www.", ""))



drops = ["city", "longitude_x", "latitude_y", "size_m2", "rooms", "bathrooms", "price"] 
clean = clean.dropDuplicates(subset=drops)

fillnas = ["size_m2", "price", "rooms", "bathrooms"]
clean = clean.fillna(0, subset=fillnas)


#Drop the entries that have no size, no price and invalid "rooms" values
nulls = clean.filter((col('size_m2') == 0) | (col('price') == 0) | (col('rooms') < 0))
clean = clean.subtract(nulls)

clean = clean.withColumn("price_per_m2", expr("price / size_m2"))


#Create a new column called "category"
housing_conditions = ["apartment", "residential", "house", "beach house"] #apartment, residentials, house, beach house
commercial_conditions = ["store", "office"] #store, office
land_condition = ["land"] #land

# Apply the conditions and assign values to "category"
clean = clean.withColumn("category", 
                   when(clean["property_type"].isin(housing_conditions), "housing")
                   .when(clean["property_type"].isin(commercial_conditions), "commercial")
                   .when(clean["property_type"].isin(land_condition), "land")
                   .otherwise("other"))

clean = clean.withColumn("scraped_on", col("scraped_on").cast("timestamp"))


#delete the properties listed more than once
window = Window.partitionBy('price', 'longitude_x', 'latitude_y', 'size_m2', 'rooms', 'bathrooms').orderBy('scraped_on')
duplicated = clean.withColumn('duplicate', row_number().over(window) > 1)
clean = duplicated.filter(~col('duplicate')).drop('duplicate')

#save the clean data into a GCS bucket
clean.write.parquet(f'gs://peru-real-state-datalake-clean/{date}', mode='overwrite')



#retriving the data from the existing bigquery database
query = '''SELECT * FROM `big-query-406221.peru_real_state.all_data` '''
existing = spark.read.format("bigquery").option("table", 'big-query-406221.peru_real_state.all_data').load(query)


columns = ['price', 'longitude_x', 'latitude_y', 'size_m2', 'rooms', 'bathrooms', 'url']
combined = clean.union(existing)
new_data = combined.dropDuplicates(columns)


new_data.write.format("bigquery") \
            .option("writeMethod" , "direct") \
            .mode('append') \
            .save("peru_real_state.all_data")

spark.stop()


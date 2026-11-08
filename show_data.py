from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("schema_check")
         .config("spark.sql.caseSensitive", "true").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

reviews = spark.read.json("data/Appliances.jsonl")
meta = spark.read.json("data/meta_Appliances.jsonl")

def schema_line(df):
    return ", ".join(f"{f.name}:{f.dataType.typeName()}" for f in df.schema.fields)

print("REVIEWS SCHEMA:", schema_line(reviews))
reviews.select("parent_asin", "user_id", "rating", "title",
               "timestamp", "helpful_vote", "verified_purchase").show(5, truncate=15)

print("METADATA SCHEMA:", schema_line(meta))
meta.select("parent_asin", "title", "store", "price",
            "average_rating", "rating_number").show(5, truncate=15)

spark.stop()

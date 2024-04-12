from pyspark.sql import SparkSession
# Create a new SparkSession and assign it to a variable named spark.
spark = SparkSession \
    .builder \
    .getOrCreate()
# Create an RDD from a list of sample clickstream counts and save it as clickstream_counts_rdd.
sample_clickstream_counts = [
    ["other-search", "Hanging_Gardens_of_Babylon", "external", 47000],
    ["other-empty", "Hanging_Gardens_of_Babylon", "external", 34600],
    ["Wonders_of_the_World", "Hanging_Gardens_of_Babylon", "link", 14000],
    ["Babylon", "Hanging_Gardens_of_Babylon", "link", 2500]
]

clickstream_counts_rdd = spark.sparkContext.parallelize(
    sample_clickstream_counts
)
# Using the RDD from the previous step, create a DataFrame named clickstream_sample_df
clickstream_sample_df = clickstream_counts_rdd\
    .toDF(["source_page", "target_page",  "link_category", "link_count"])

# Display the DataFrame to the notebook
clickstream_sample_df.show(5, truncate=False)
+--------------------+--------------------------+-------------+----------+
|source_page         |target_page               |link_category|link_count|
+--------------------+--------------------------+-------------+----------+
|other-search        |Hanging_Gardens_of_Babylon|external     |47000     |
|other-empty         |Hanging_Gardens_of_Babylon|external     |34600     |
|Wonders_of_the_World|Hanging_Gardens_of_Babylon|link         |14000     |
|Babylon             |Hanging_Gardens_of_Babylon|link         |2500      |
+--------------------+--------------------------+-------------+----------+

#Read the files in ./cleaned/clickstream/ into a new Spark DataFrame named clickstream and display the first few rows of the DataFrame in the notebook
clickstream = spark.read \
    .option('header', True) \
    .option('delimiter', '\t') \
    .option('inferSchema', True) \
    .csv("./cleaned/clickstream/")

# Display the DataFrame to the notebook
clickstream.show(5, truncate=False)
+-------------------+--------------+-------------+-------------+-----------+
|referrer           |resource      |link_category|language_code|click_count|
+-------------------+--------------+-------------+-------------+-----------+
|Daniel_Day-Lewis   |Phantom_Thread|link         |en           |43190      |
|other-internal     |Phantom_Thread|external     |en           |21683      |
|other-empty        |Phantom_Thread|external     |en           |169532     |
|90th_Academy_Awards|Phantom_Thread|link         |en           |40449      |
|other-search       |Phantom_Thread|external     |en           |536940     |
+-------------------+--------------+-------------+-------------+-----------+
only showing top 5 rows

# Display the schema of the `clickstream` DataFrame to the notebook
clickstream.printSchema()
root
 |-- referrer: string (nullable = true)
 |-- resource: string (nullable = true)
 |-- link_category: string (nullable = true)
 |-- language_code: string (nullable = true)
 |-- click_count: integer (nullable = true)

#Drop the language_code column from the DataFrame and display the new schema in the notebook.
clickstream = clickstream.drop("language_code")

# Display the first few rows of the DataFrame and the new schema in the notebook
clickstream.show(5, truncate=False)
clickstream.printSchema()
+-------------------+--------------+-------------+-----------+
|referrer           |resource      |link_category|click_count|
+-------------------+--------------+-------------+-----------+
|Daniel_Day-Lewis   |Phantom_Thread|link         |43190      |
|other-internal     |Phantom_Thread|external     |21683      |
|other-empty        |Phantom_Thread|external     |169532     |
|90th_Academy_Awards|Phantom_Thread|link         |40449      |
|other-search       |Phantom_Thread|external     |536940     |
+-------------------+--------------+-------------+-----------+
only showing top 5 rows

root
 |-- referrer: string (nullable = true)
 |-- resource: string (nullable = true)
 |-- link_category: string (nullable = true)
 |-- click_count: integer (nullable = true)

#Rename referrer and resource to source_page and target_page, respectively
clickstream = clickstream\
    .withColumnRenamed("referrer", "source_page")\
    .withColumnRenamed("resource", "target_page")
  
# Display the first few rows of the DataFrame and the new schema in the notebook
clickstream.show(5, truncate=False)
clickstream.printSchema()
+-------------------+--------------+-------------+-----------+
|source_page        |target_page   |link_category|click_count|
+-------------------+--------------+-------------+-----------+
|Daniel_Day-Lewis   |Phantom_Thread|link         |43190      |
|other-internal     |Phantom_Thread|external     |21683      |
|other-empty        |Phantom_Thread|external     |169532     |
|90th_Academy_Awards|Phantom_Thread|link         |40449      |
|other-search       |Phantom_Thread|external     |536940     |
+-------------------+--------------+-------------+-----------+
only showing top 5 rows

root
 |-- source_page: string (nullable = true)
 |-- target_page: string (nullable = true)
 |-- link_category: string (nullable = true)
 |-- click_count: integer (nullable = true)

#Rename referrer and resource to source_page and target_page, respectively
clickstream = clickstream\
    .withColumnRenamed("referrer", "source_page")\
    .withColumnRenamed("resource", "target_page")
  
# Display the first few rows of the DataFrame and the new schema in the notebook
clickstream.show(5, truncate=False)
clickstream.printSchema()
+-------------------+--------------+-------------+-----------+
|source_page        |target_page   |link_category|click_count|
+-------------------+--------------+-------------+-----------+
|Daniel_Day-Lewis   |Phantom_Thread|link         |43190      |
|other-internal     |Phantom_Thread|external     |21683      |
|other-empty        |Phantom_Thread|external     |169532     |
|90th_Academy_Awards|Phantom_Thread|link         |40449      |
|other-search       |Phantom_Thread|external     |536940     |
+-------------------+--------------+-------------+-----------+
only showing top 5 rows

root
 |-- source_page: string (nullable = true)
 |-- target_page: string (nullable = true)
 |-- link_category: string (nullable = true)
 |-- click_count: integer (nullable = true)

#Add the clickstream DataFrame as a temporary view named clickstream
# Create a temporary view in the metadata for this `SparkSession` to make the data
# queryable with `sparkSession.sql()`
clickstream.createOrReplaceTempView("clickstream")

#Filter the dataset to entries with Hanging_Gardens_of_Babylon as the target_page and order the result by click_count using PySpark DataFrame methods.
# Filter and sort the DataFrame using PySpark DataFrame methods
clickstream\
    .filter(clickstream.target_page == 'Hanging_Gardens_of_Babylon')\
    .orderBy('click_count', ascending=False)\
    .show(10, truncate=False)
+----------------------------------+--------------------------+-------------+-----------+
|source_page                       |target_page               |link_category|click_count|
+----------------------------------+--------------------------+-------------+-----------+
|other-search                      |Hanging_Gardens_of_Babylon|external     |47088      |
|other-empty                       |Hanging_Gardens_of_Babylon|external     |34619      |
|Wonders_of_the_World              |Hanging_Gardens_of_Babylon|link         |14668      |
|Seven_Wonders_of_the_Ancient_World|Hanging_Gardens_of_Babylon|link         |12296      |
+----------------------------------+--------------------------+-------------+-----------+

#Perform the same analysis as the previous exercise using a SQL query.
# Filter and sort the DataFrame using SQL
spark.sql(
    """
    SELECT *
    FROM clickstream
    WHERE target_page = 'Hanging_Gardens_of_Babylon'
    ORDER BY click_count DESC
    """
).show(10, truncate=False)
+----------------------------------+--------------------------+-------------+-----------+
|source_page                       |target_page               |link_category|click_count|
+----------------------------------+--------------------------+-------------+-----------+
|other-search                      |Hanging_Gardens_of_Babylon|external     |47088      |
|other-empty                       |Hanging_Gardens_of_Babylon|external     |34619      |
|Wonders_of_the_World              |Hanging_Gardens_of_Babylon|link         |14668      |
|Seven_Wonders_of_the_Ancient_World|Hanging_Gardens_of_Babylon|link         |12296      |
+----------------------------------+--------------------------+-------------+-----------+

#Calculate the sum of click_count grouped by link_category using PySpark DataFrame methods.
# Aggregate the DataFrame using PySpark DataFrame Methods 
clickstream\
    .groupBy('link_category')\
    .sum()\
    .show(truncate=False)
+-------------+----------------+
|link_category|sum(click_count)|
+-------------+----------------+
|link         |97805811        |
|other        |9338172         |
|external     |3248677856      |
+-------------+----------------+

#Perform the same analysis as the previous exercise using a SQL query.
# Aggregate the DataFrame using SQL
spark.sql(
    """
    SELECT link_category, SUM(click_count) FROM clickstream
    GROUP BY link_category
    """
).show(truncate=False)
+-------------+----------------+
|link_category|sum(click_count)|
+-------------+----------------+
|link         |97805811        |
|other        |9338172         |
|external     |3248677856      |
+-------------+----------------+

#Let's create a new DataFrame named internal_clickstream that only contains article pairs where link_category is link.
# Create a new DataFrame (named `internal_clickstream`) using `filter` to select rows to 
# a specific condition and `select` to choose which columns to return from the query.
internal_clickstream = clickstream\
    .select(["source_page", "target_page", "click_count"])\
    .filter(clickstream.link_category == 'link')

# Display the first few rows of the DataFrame in the notebook
internal_clickstream.show(truncate=False)
+----------------------------+----------------------------+-----------+
|source_page                 |target_page                 |click_count|
+----------------------------+----------------------------+-----------+
|Daniel_Day-Lewis            |Phantom_Thread              |43190      |
|90th_Academy_Awards         |Phantom_Thread              |40449      |
|Shinee                      |Kim_Jong-hyun_(singer)      |24433      |
|Agnyaathavaasi              |Anu_Emmanuel                |15020      |
|Naa_Peru_Surya              |Anu_Emmanuel                |12361      |
|Mariah_Carey                |Nick_Cannon                 |16214      |
|Kesha                       |Rainbow_(Kesha_album)       |11448      |
|David_Attenborough          |John_Attenborough           |11252      |
|Boney_M.                    |Bobby_Farrell               |14095      |
|The_End_of_the_F***ing_World|Jessica_Barden              |237279     |
|Quentin_Tarantino           |The_Hateful_Eight           |12018      |
|Ready_Player_One_(film)     |Olivia_Cooke                |17468      |
|Royal_Rumble_(2018)         |Kevin_Owens_and_Sami_Zayn   |11503      |
|Macaulay_Culkin             |Brenda_Song                 |20477      |
|Altered_Carbon              |Altered_Carbon_(TV_series)  |23962      |
|Lil_Pump                    |Smokepurpp                  |36736      |
|Fifth_Harmony               |Camila_Cabello              |30959      |
|Havana_(Camila_Cabello_song)|Camila_Cabello              |12803      |
|Jennifer_Aniston            |John_Aniston                |26498      |
|Kingsman:_The_Golden_Circle |Kingsman:_The_Secret_Service|11969      |
+----------------------------+----------------------------+-----------+
only showing top 20 rows

#Save the internal_clickstream DataFrame as CSV files in a directory called ./results/article_to_article_csv/
# Save the `internal_clickstream` DataFrame to a series of CSV files in `./results/article_links_csv/`
# with `DataFrame.write.csv()`
internal_clickstream\
    .write\
    .csv('./results/article_links_csv/', mode="overwrite")

#Save the internal_clickstream DataFrame as parquet files in a directory called ./results/article_to_article_pq/
# Save the `internal_clickstream` DataFrame to a series of parquet files in `./results/article_links_parquet/`
# with `DataFrame.write.parquet()`

internal_clickstream\
    .write\
    .parquet('./results/article_links_parquet/', mode="overwrite")

#Close the SparkSession and underlying sparkContext. What happens if you we call clickstream.show() after closing the SparkSession?
# Stop the notebook's `SparkSession` and `SparkContext`
spark.stop()
# The SparkSession and sparkContext are stopped; the following line will throw 
# an error:
clickstream.show()




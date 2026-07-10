from pyspark.sql.session import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler

spark = (SparkSession.builder
         .appName("LinearRegression")
         .getOrCreate())

# Sample data 
data = [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
df = spark.createDataFrame(data, ["feature", "label"])

# Assemble features
assembler = VectorAssembler(inputCols=["feature"], outputCol="features")
df = assembler.transform(df)

# Create linear regression model
lr = LinearRegression(featuresCol="features", labelCol="label", predictionCol="prediction")

# Fit the model
model = lr.fit(df)

# Print coefficients and intercept
print("Coefficients: %s" % str(model.coefficients))
print("Intercept: %f" % model.intercept)

spark.stop()

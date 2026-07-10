# Spark + Python image (adjust tag to your Spark version)
FROM apache/spark-py

USER root

# Add Python libs you need
RUN pip install --no-cache-dir pandas numpy matplotlib

# Put your script into the image
WORKDIR /workspace
COPY workspace/linear_regression.py /workspace/linear_regression.py




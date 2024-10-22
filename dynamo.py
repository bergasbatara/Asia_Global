import json
import boto3
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')

# Replace 'your_table_name' with your DynamoDB table name
table_name = 'Sample_Data'
table = dynamodb.Table(table_name)

# Function to read and transform NDJSON data
def read_ndjson(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line, parse_float=Decimal)  # Parse floats as Decimals

# Transform the NDJSON data for DynamoDB
dynamodb_data = []
for item in read_ndjson('exported_data.json'):
    dynamo_item = {
        'PrimaryKey': item['_id']['$oid'],  # Using MongoDB's _id as the partition key
        'Date': item['Date'],
        'Time': item['Time'],
        'Product_ID': int(item['Product_ID']),  # Ensure Product_ID is an integer
        'Quantity': int(item['Quantity']),  # Ensure Quantity is an integer
        'Price': Decimal(str(item['Price'])),  # Convert Price to Decimal
        'Category': item['Category']
    }
    dynamodb_data.append(dynamo_item)

# Function to import data into DynamoDB
def import_data_to_dynamodb(data, table):
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

# Import the transformed data into DynamoDB
import_data_to_dynamodb(dynamodb_data, table)

print("Data import completed successfully.")
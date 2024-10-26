import json
import boto3
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')  # Use your AWS region

# Replace 'your_table_name' with your DynamoDB table name
table_name = 'Sample_Data'  # Replace with your table name
table = dynamodb.Table(table_name)

# Function to read and transform NDJSON data
def read_ndjson(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line, parse_float=Decimal)  # Parse floats as Decimals

# Transform the NDJSON data for DynamoDB
dynamodb_data = []
for item in read_ndjson('exported_data.json'):
    try:
        # Make sure the partition and sort key names match your DynamoDB table schema
        dynamo_item = {
            'id': item['_id']['$oid'],  # Partition Key (String)
            'Product_id': str(item['Product_ID']),  # Sort Key (String)
            'Date': item['Date'],
            'Time': item['Time'],
            'Quantity': Decimal(str(item['Quantity'])),  # Convert Quantity to Decimal
            'Price': Decimal(str(item['Price'])),  # Convert Price to Decimal
            'Category': item['Category']
        }
        print(f"Prepared DynamoDB item: {dynamo_item}")  # Debugging output
        dynamodb_data.append(dynamo_item)
    except Exception as e:
        print(f"Error processing item: {item} - {e}")

# Function to import data into DynamoDB
def import_data_to_dynamodb(data, table):
    with table.batch_writer() as batch:
        for item in data:
            try:
                batch.put_item(Item=item)
                print(f"Successfully added item: {item}")  # Debugging output
            except Exception as e:
                print(f"Error adding item to DynamoDB: {item} - {e}")

# Import the transformed data into DynamoDB
import_data_to_dynamodb(dynamodb_data, table)

print("Data import attempt completed.")
import boto3
import json

def get_cypher_key(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1",
    )

    get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
   
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)["dfk-secret-key"]

import boto3
import os;
from botocore.exceptions import ClientError;
def setUp(self):
        # Initialize AWS clients
        self.lambda_client = boto3.client('lambda', region_name='us-east-1')
        self.s3_client = boto3.client('s3', region_name='us-east-1')
        
        # Upload a test file to Lambda
        self.test_file_key = 'test_file.txt'
        self.test_file_content = b'This is a test file content.'

        # Create a bucket in S3
        self.bucket_name =os.environ.get('DestinationBucketName')
        self.s3_client.create_bucket(Bucket=self.bucket_name)
#testcase1
def test_lambda_s3_upload(self):
        # Upload the test file to Lambda
        self.lambda_client.invoke(
            FunctionName='lambda_handler',
            InvocationType='Event',
            Payload=self.test_file_content
        )
        
        # Check if the file was uploaded to S3
        s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.test_file_key)
        print(s3_object)
        self.assertIsNotNone(s3_object)
#testcase2
def test_lambda_s3_download(self):
        #Download the file from S3
        s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.test_file_key)
        downloaded_content = s3_object['Body'].read().decode('utf-8')
        # Verify the downloaded content matches the uploaded content
        self.assertEqual(downloaded_content, self.test_file_content.decode('utf-8'))

#testcase3
def test_lambda_s3_delete_file(self):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.test_file_key)
        # Verify that the file is deleted
        with self.assertRaises(Exception):
         self.s3_client.head_object(Bucket=self.bucket_name, Key=self.test_file_key)
#testcase4
def test_lambda_s3_upload_invalid_path(self):
        lambda_function_name = 'lambda_handler'
        response = self.lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',
            Payload=b'{"file_path": "invalid/path/to/file.txt"}'  # Pass an invalid file path
        )
        self.assertEqual(response['StatusCode'], 200)
        
        # Check if the file was not uploaded to S3
        with self.assertRaises(Exception):  # Assuming Lambda throws an exception for invalid file paths
            self.s3_client.get_object(Bucket=self.bucket_name, Key=self.test_file_key)
#testcase5
def test_lambda_s3_upload_invalid_bucket_name(self):
        invalid_bucket_name = 'invalid-bucket-name'
        
        # Invoke the Lambda function with the invalid bucket name
        lambda_function_name = 'your-lambda-function-name'
        with self.assertRaises(Exception) as context:
            response = self.lambda_client.invoke(
                FunctionName=lambda_function_name,
                InvocationType='RequestResponse',
                Payload=b'{"bucket_name": "' + invalid_bucket_name.encode('utf-8') + b'"}' 
            )
        
        # Check if Lambda execution failed due to the invalid bucket name
        self.assertIn("The specified bucket does not exist", str(context.exception))

#testcase6
def test_access_denied(self):
    # Initialize an S3 client with incorrect credentials or insufficient permissions
    s3 = boto3.client('s3', region_name='your-region', aws_access_key_id='valid-access-key', aws_secret_access_key='valid-secret-key')

    try:
        response = s3.get_object(Bucket=self.bucket_name, Key=self.test_file_key)
    except ClientError as e:
        # Handle the access denied error
        if e.response['Error']['Code'] == 'AccessDenied':
            print("Access denied error encountered.")
        else:
            print("Error:", e)
    else:
        print("Object retrieved successfully:", response)


def tearDown(self):
        # Clean up by deleting the test file from S3
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.test_file_key)
        # Clean up by deleting the bucket
        self.s3_client.delete_bucket(Bucket=self.bucket_name)


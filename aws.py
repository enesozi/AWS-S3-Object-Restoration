import boto3
import botocore

# Each line in keys files represents an object in a bucket
file_names = ["keys_file_1.txt","keys_file_2.txt"]

# You can get all of your buckets by following command
# s3.buckets.all()
bucket_names = ["bucket_name_1","bucket_name_2"]

# To keep an index on bucket_ names
bucket_index = 0

# Let's use Amazon S3
s3 = boto3.resource('s3')

for file in file_names:
	f = open(file, 'r')
	key_names = f.read().splitlines()
	bucket = s3.Bucket(bucket_names[bucket_index])
	for key in key_names:
		try:
			full_key = bucket.Object(key).load()
		except botocore.exceptions.ClientError as ex:
			if ex.response['Error']['Code'] == '404':
				print(key + ' does not exist')
		else:
			full_key = bucket.Object(key)
			if full_key.restore is None and full_key.storage_class == "GLACIER":
				resp = bucket.meta.client.restore_object(Bucket=bucket_names[bucket_index],Key=key,RestoreRequest={'Days': 2})
				print(resp)
	bucket_index = bucket_index + 1
from botocore.exceptions import NoCredentialsError

import boto3
import numpy as np
import os

def send_files(files, credentials, bucket, send_all = True):
    """
        Parameters:
        files (list of strings): All the files that will be sent to the AWS bucket.
        sender (dict): Dictionary with AWS credentials.
        bucket (string): A string specifying the bucket in S3.
        send_all (bool): Determine if it sends all files or randomly select two of them.
    """
    print(files)
    s3 = boto3.client("s3", 
                        aws_access_key_id = credentials["ACCESS_KEY"],
                        aws_secret_access_key = credentials["SECRET_KEY"])

    files = (np.random.choice(files, size = 2, replace = False) 
                    if not send_all else files)
    
    for file in files:
        folder = os.path.dirname(file).split(os.sep)[-1]
        file_name = os.path.basename(file)
        aws_file = "{}/{}".format(folder, file_name)
        try:
            s3.upload_file(file, bucket, aws_file)
            print("Uploaded file {} to S3 bucket.".format(aws_file))
        except NoCredentialsError:
            print("Credentials not valid")



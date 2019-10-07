# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config


def delete_object(bucket_name, object_name):
    """Delete an object from an S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: True if the referenced object was deleted, otherwise False
    """

    # Delete the object
    s3 = boto3.resource('s3', config=Config(  # Force a retry after 3 seconds rather than 60
        connect_timeout=3, read_timeout=3, retries={'max_attempts': 2}))
    obj = s3.Object(bucket_name, object_name)
    try:
        obj.delete()
    except ClientError as e:
        logging.error(e)
        return False
    return True
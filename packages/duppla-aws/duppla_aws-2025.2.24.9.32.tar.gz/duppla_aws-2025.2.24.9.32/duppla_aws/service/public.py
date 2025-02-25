import boto3
from types_boto3_amplify import AmplifyClient
from duppla_aws.service._cloudformation import CloudFormationResource
from duppla_aws.service._cloudwatch import CloudWatchResource
from duppla_aws.service._dynamodb import DynamoDBResource
from duppla_aws.service._s3 import S3Resource


class AmazonWebServices:
    def __init__(
        self, aws_access_key_id: str, aws_secret: str, aws_region: str = "us-east-1"
    ) -> None:
        _session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )

        self.s3 = S3Resource(
            client=_session.client("s3"),
            resource=_session.resource("s3"),
        )
        """The connection to the S3 bucket service"""
        self.dynamo = DynamoDBResource(
            client=_session.client("dynamodb"),
            resource=_session.resource("dynamodb"),
        )
        """The connection to the DynamoDB service"""
        DynamoDBResource._upload_and_insert.f_put_object = self.s3.put_object  # pyright: ignore[reportPrivateUsage, reportFunctionMemberAccess]
        self.cloudformation = CloudFormationResource(
            client=_session.client("cloudformation"),
            resource=_session.resource("cloudformation"),
        )
        """The connection to the CloudFormation service"""
        self.cloudwatch = CloudWatchResource(
            client=_session.client("cloudwatch"),
            resource=_session.resource("cloudwatch"),
        )
        """The connection to the CloudWatch service"""
        self.amplify: AmplifyClient = _session.client("amplify")
        """The connection to the Amplify service"""

        self._session = _session
        """The boto3 session object, for custom use"""

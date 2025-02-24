from typing import Literal, Optional, Sequence, Union, overload

from types_boto3_s3 import S3ServiceResource
from types_boto3_s3.literals import ObjectCannedACLType
from types_boto3_s3.service_resource import ObjectSummary
from types_boto3_s3.type_defs import BlobTypeDef


class S3Resource(S3ServiceResource):
    def get_object(self, bucket: str, filename: str):
        return self.Object(bucket, filename).get()

    def put_object(
        self, bucket: str, filename: str,
        body: BlobTypeDef, acl: ObjectCannedACLType = "public-read"
    ):  # fmt:skip
        return self.Object(bucket, filename).put(Body=body, ACL=acl)

    def change_object_acl(
        self, bucket: str, filename: str,
        acl: ObjectCannedACLType = "public-read"
    ):  # fmt:skip
        return self.Object(bucket, filename).Acl().put(ACL=acl)

    @overload
    def get_by_criteria(
        self, bucket: str, *, filename: str, url: Literal[False]
    ) -> Optional[ObjectSummary]: ...

    @overload
    def get_by_criteria(
        self, bucket: str, *, extensions: Sequence[str], url: Literal[False]
    ) -> list[ObjectSummary]: ...

    @overload
    def get_by_criteria(
        self, bucket: str, *, extension: str, url: Literal[False]
    ) -> list[ObjectSummary]: ...

    @overload
    def get_by_criteria(
        self, bucket: str, *, filename: str, url: Literal[True]
    ) -> Optional[str]: ...

    @overload
    def get_by_criteria(
        self, bucket: str, *, extensions: Sequence[str], url: Literal[True]
    ) -> list[str]: ...

    @overload
    def get_by_criteria(
        self, bucket: str, *, extension: str, url: Literal[True]
    ) -> list[str]: ...

    def get_by_criteria(
        self,
        bucket: str,
        *,
        filename: Optional[str] = None,
        extensions: Optional[Sequence[str]] = None,
        extension: Optional[str] = None,
        url: bool = False,
    ) -> Union[ObjectSummary, str, list[ObjectSummary], list[str], None]:
        """
        This method is designed to get a object from a bucket in s3 by a criteria
        The criteria can be the filename or the extension of the file
        If the criteria is the filename, the method will return the object
        If the criteria is the extension, the method will return a list of objects

        Args:
            bucket (str): The name of the bucket
            filename (Optional[str], optional): The filename of the object. Defaults to None.
            extension (Optional[str], optional): The extension of the object. Defaults to None.
        """
        bucket_objects = self.Bucket(bucket).objects.all()
        if filename:
            file_obj = next(
                (obj for obj in bucket_objects if obj.key == filename), None
            )
            if file_obj:
                return (
                    f"https://{bucket}.s3.amazonaws.com/{file_obj.key}"
                    if url
                    else file_obj
                )
            return None

        if extensions is None:
            extensions = [extension] if extension else ["jpg", "jpeg", "png"]
        extensions = tuple(ext.lower() for ext in extensions)

        files_obj = [
            obj for obj in bucket_objects if obj.key.lower().endswith(extensions)
        ]

        if not files_obj:
            return []

        return (
            [f"https://{bucket}.s3.amazonaws.com/{obj.key}" for obj in files_obj]
            if url
            else files_obj
        )

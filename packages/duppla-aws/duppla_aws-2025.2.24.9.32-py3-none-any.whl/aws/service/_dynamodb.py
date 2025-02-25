import uuid
from datetime import datetime
from decimal import Decimal

from types_boto3_dynamodb import DynamoDBServiceResource
from types_boto3_dynamodb.type_defs import (
    ConditionBaseImportTypeDef,
    TableAttributeValueTypeDef,
)

from duppla_aws.utils.encoder import JSON, jsonable_dumps


class DynamoDBResource(DynamoDBServiceResource):
    def get_table(self, tablename: str):
        return self.Table(tablename)

    def query(
        self,
        tablename: str,
        *,
        index: str,
        condition_expression: ConditionBaseImportTypeDef,
        expression_values: dict[str, TableAttributeValueTypeDef],
    ):
        return self.Table(tablename).query(
            IndexName=index,
            KeyConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_values,
        )

    def scan(
        self,
        tablename: str,
        *,
        filter: ConditionBaseImportTypeDef,
        expression_values: dict[str, TableAttributeValueTypeDef],
    ):
        return self.Table(tablename).scan(
            FilterExpression=filter,
            ExpressionAttributeValues=expression_values,
        )

    def get_item(
        self,
        table: str,
        key: dict[str, TableAttributeValueTypeDef],
        **kwargs: TableAttributeValueTypeDef,
    ):
        return self.Table(table).get_item(Key={**key, **kwargs})

    @staticmethod
    def _convert_to_table_attribute(obj: JSON) -> JSON:
        if isinstance(obj, dict):
            return {
                k: DynamoDBResource._convert_to_table_attribute(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [
                DynamoDBResource._convert_to_table_attribute(element) for element in obj
            ]
        elif isinstance(obj, float):
            return Decimal(str(obj))  # pyright: ignore[reportReturnType]
        else:
            return obj

    def insert(self, tablename: str, item: JSON):
        if len(jsonable_dumps(item)) >= 40_000:
            self.insert_over_40kb(tablename, item)
            return {"status": "success"}

        tableobj = self.get_table(tablename)
        item = self._convert_to_table_attribute(item)

        if isinstance(item, dict):
            response = tableobj.put_item(Item=item, ReturnValues="ALL_OLD")  # pyright:ignore[reportArgumentType]
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code != 200:
                raise IOError(f"Error inserting item into table {tablename}")
            return response["ResponseMetadata"]
        elif isinstance(item, list):
            with tableobj.batch_writer() as batch:
                for i in item:
                    batch.put_item(Item=i)  # pyright:ignore[reportArgumentType]
                return {"status": "success"}
        else:
            raise ValueError("Item must be a structred json")

    def insert_over_40kb(self, tablename: str, item: JSON):
        if isinstance(item, list):
            for i, item_obj in enumerate(item):
                self.insert_over_40kb(f"{tablename}_{i}", item_obj)
        elif isinstance(item, dict):
            for key, value in item.items():
                if len(jsonable_dumps(value)) > 40000:
                    self._upload_and_insert(tablename, key, value)
                else:
                    self.insert(tablename, value)  # type: ignore
        else:
            self._upload_and_insert(tablename, str(uuid.uuid4()), item)

    def _upload_and_insert(self, tablename: str, key: str, value: JSON):
        filename = f"{key.removesuffix('.json')}_{datetime.now().isoformat()}.json"
        DynamoDBResource._upload_and_insert.f_put_object(  # pyright: ignore[reportFunctionMemberAccess]
            tablename, filename, jsonable_dumps(value)
        )
        self.insert(
            filename,
            {"id": filename, "data_location": f"s3://{tablename}/{filename}"},
        )

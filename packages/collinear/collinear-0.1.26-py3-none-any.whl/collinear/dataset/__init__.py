import json
import uuid

import aiohttp
import pandas as pd

from collinear.BaseService import BaseService
from collinear.dataset.types import UploadDatasetResponseType


class Dataset(BaseService):
    def __init__(self, access_token: str, space_id: str) -> None:
        super().__init__(access_token, space_id)

    async def upload_dataset(self, data: pd.DataFrame,
                             conv_prefix_column_name: str,
                             response_column_name: str,
                             ground_truth_column_name: str | None,
                             dataset_name: str) -> UploadDatasetResponseType:
        """
        Uploads a dataset to the Collinear platform.
        Args:
            data: A pandas DataFrame containing the dataset.
            conv_prefix_column_name: Name of the column containing the conversation prefix.
            response_column_name: Name of the column containing the response.
            ground_truth_column_name: Name of the column containing the ground truth. If not provided, the column will be ignored.
            dataset_name: Name of the dataset.

        Returns:
            UploadDatasetResponseType: ID of the uploaded dataset and rows.
        """

        conversations = []
        for _, row in data.iterrows():
            obj = {
                'conv_prefix': list(row[conv_prefix_column_name]),
                'response': row[response_column_name],
                'ground_truth': row[
                    ground_truth_column_name] if ground_truth_column_name and ground_truth_column_name in row else {}
            }
            conversations.append(obj)
        json_file_name = "dataset.json"
        with open(json_file_name, "w") as json_file:
            json.dump(conversations, json_file)
        with open(json_file_name, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=json_file_name, content_type='application/json')
            form_data.add_field('dataset_name', dataset_name)
            resp = await self.send_form_request('/api/v1/dataset/upload', form_data, "POST")
            return UploadDatasetResponseType(dataset_id=resp['data_id'], dataset=resp['data'])

    async def upload_assessed_dataset(self, data: pd.DataFrame,
                                      evaluation_name: str,
                                      dataset_id: str) -> str:
        """
        Uploads a dataset to the Collinear platform.
        Args:
            data: A pandas DataFrame containing the dataset.
            evaluation_name: Name of the evaluation.
            dataset_id: ID of the dataset.

        Returns:
            dataset_id: ID of the uploaded dataset.
        """

        conversations = []
        for _, row in data.iterrows():
            obj = {
                'id': row['id'],
                'judgement': row['judgement']
            }
            conversations.append(obj)
        json_file_name = "dataset.json"
        with open(json_file_name, "w") as json_file:
            json.dump(conversations, json_file)
        with open(json_file_name, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=json_file_name, content_type='application/json')
            form_data.add_field('evaluation_name', evaluation_name)
            form_data.add_field('dataset_id', dataset_id)
            resp = await self.send_form_request('/api/v1/dataset/assess/upload', form_data, "POST")
            return resp['data']['data']['evaluation_id']

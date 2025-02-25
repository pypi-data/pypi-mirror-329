from typing import Optional
import pandas as pd
from datetime import datetime

from .base import SodecoBase
from .schemas.contract import ContractSchema, CareerBreakSchema, CertainWorkSchema, StudentSchema
from .schemas import DATEFORMAT
from brynq_sdk_functions import Functions


class Contracts(SodecoBase):
    """Class for managing contracts in Sodeco."""

    def __init__(self, sodeco):
        super().__init__(sodeco)
        self.url = f"{self.sodeco.base_url}worker"

    def get(self, worker_id: str, ref_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get contract information for a worker, optionally at a specific reference date.
        
        Args:
            worker_id: The worker ID to get contract for
            ref_date: Optional reference date to get contract state at
            
        Returns:
            pd.DataFrame: DataFrame containing the contract information
        """
        url = f"{self.url}/{worker_id}/contract"
        if ref_date is not None:
            url += f"/{ref_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)

    def validate_nested_fields(self, payload: dict, debug: bool = False) -> dict:
        """
        Validate nested fields within a contract entry.
        
        Args:
            payload: Contract dictionary containing nested fields to validate
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: Contract dictionary with validated nested fields
            
        Raises:
            ValueError: If any nested field is invalid
        """
        # Make a copy to avoid modifying the original
        validated_payload = payload.copy()
        
        # Helper function to validate nested field
        def validate_nested(field_name: str, schema_class) -> None:
            if field_data := validated_payload.get(field_name):
                # Convert to dict if it's a Series
                if hasattr(field_data, 'to_dict'):
                    field_data = field_data.to_dict()
                df = pd.DataFrame([field_data])
                valid_data, invalid_data = Functions.validate_data(df, schema_class, debug=debug)
                if len(invalid_data) > 0:
                    error_msg = f"Invalid {field_name} data"
                    if debug:
                        error_msg += f": {invalid_data.to_dict(orient='records')}"
                    raise ValueError(error_msg)
                validated_payload[field_name] = valid_data.iloc[0].to_dict()
        
        # Validate each nested field
        validate_nested('CareerBreak', CareerBreakSchema)
        validate_nested('CertainWork', CertainWorkSchema)
        validate_nested('Student', StudentSchema)
            
        return validated_payload

    def create(self, worker_id: str, payload: dict, debug: bool = False) -> dict:
        """
        Create a contract for a worker.
        The payload must adhere to the structure defined by the ContractSchema.
        
        Args:
            worker_id: The ID of the worker to create a contract for
            payload: The contract data to create
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: The created contract data
            
        Raises:
            ValueError: If the payload is invalid
        """
        url = f"{self.url}/{worker_id}/contract"
        
        # Convert payload to DataFrame and validate
        df = pd.DataFrame([payload])
        valid_data, invalid_data = Functions.validate_data(df, ContractSchema, debug=debug)

        if len(invalid_data) > 0:
            error_msg = "Invalid contract payload"
            if debug:
                error_msg += f": {invalid_data.to_dict(orient='records')}"
            raise ValueError(error_msg)

        # Validate nested fields
        valid_data.iloc[0] = self.validate_nested_fields(valid_data.iloc[0].to_dict(), debug=debug)

        # Send the POST request to create the contract
        headers, data = self._prepare_raw_request(valid_data.iloc[0].to_dict())
        data = self._make_request_with_polling(
            url,
            method='POST',
            headers=headers,
            data=data
        )
        return data

    def update(self, worker_id: str, contract_date: datetime, payload: dict, debug: bool = False) -> dict:
        """
        Update a contract for a worker.
        The payload must adhere to the structure defined by the ContractSchema.
        
        Args:
            worker_id: The ID of the worker who owns the contract
            contract_date: The start date of the contract to update
            payload: The contract data to update
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: The updated contract data
            
        Raises:
            ValueError: If the payload is invalid
        """
        url = f"{self.url}/{worker_id}/contract/{contract_date.strftime(DATEFORMAT)}"
        
        # Validate the payload
        df = pd.DataFrame([payload])
        valid_data, invalid_data = Functions.validate_data(df, ContractSchema, debug=debug)

        if len(invalid_data) > 0:
            error_msg = "Invalid contract payload"
            if debug:
                error_msg += f": {invalid_data.to_dict(orient='records')}"
            raise ValueError(error_msg)

        # Validate nested fields
        valid_data.iloc[0] = self.validate_nested_fields(valid_data.iloc[0].to_dict(), debug=debug)

        # Send the PUT request to update the contract
        headers, data = self._prepare_raw_request(valid_data.iloc[0].to_dict())
        data = self._make_request_with_polling(
            url,
            method='PUT',
            headers=headers,
            data=data
        )
        return data

    def delete(self, worker_id: str, contract_date: datetime) -> dict:
        """
        Delete a contract entry for a worker.
        
        Args:
            worker_id: The ID of the worker who owns the contract
            contract_date: The start date of the contract to delete
            
        Returns:
            dict: The response from the server
        """
        url = f"{self.url}/{worker_id}/contract/{contract_date.strftime(DATEFORMAT)}"
        
        # Send the DELETE request
        data = self._make_request_with_polling(
            url,
            method='DELETE'
        )
        return data

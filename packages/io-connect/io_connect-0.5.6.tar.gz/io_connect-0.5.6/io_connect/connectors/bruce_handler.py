# External Imports
import requests
from typeguard import typechecked
import io_connect.constants as c
from typing import Optional
import json


@typechecked
class BruceHandler:
    __version__ = c.VERSION

    def __init__(
        self,
        user_id: str,
        data_url: str,
        on_prem: Optional[bool] = False,
    ):
        self.user_id = user_id
        self.data_url = data_url
        self.header = {"userID": user_id}
        self.on_prem = on_prem

    def add_insight_result(
        self,
        insight_id: str,
        workbench_id: str,
        result: list,
        devID: str,
        whitelisted_users: list,
        metadata: dict,
        tags: list,
        on_prem: Optional[bool] = None,
    ) -> bool:
        """
        Adds an insight result.

        This function adds an insight result using the specified parameters.

        Args:
            insight_id (str): The ID of the insight.
            workbench_id (str): The ID of the workbench.
            result (list): List of results.
            devID (str): Parameters related to the result.
            class_type (str): Metadata related to the result.
            tags (list): List of tags associated with the result.

        Returns:
            bool: True if the result was added successfully, False otherwise.
        Example:
            # Instantiate BruceHandler
            >>> bruce_handler = BruceHandler(data_url="example.com", user_id="userID")

            # Example: Adding an insight result
            >>> insight_added = bruce_handler.add_insight_result(
            ...     insight_id="insightID",
            ...     workbench_id="workbenchID",
            ...     result=["result1", "result2"],
            ...     devID="devID",
            ...     class_type="class type",
            ...     tags=['tags']
            ... )

        """
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.ADD_INSIGHT_RESULT.format(
                protocol=protocol,
                data_url=self.data_url,
            )

            # Prepare the request payload
            payload = {
                "insightID": insight_id,
                "workbenchID": workbench_id,
                "result": result,
                "parameters": {"devID": devID},
                "metadata": metadata,
                "whitelistedUIsers": whitelisted_users,
                "tags": tags,
            }

            # Send the request via HTTP POST with headers
            response = requests.post(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            return True

        except (TypeError, ValueError, requests.exceptions.RequestException) as e:
            print(f"[EXCEPTION] {type(e).__name__}: {e}")
            return False

        except Exception as e:
            print(f"[EXCEPTION] {e}")
            return False

    def get_insight_results(
        self, insight_id: str, count: int = 1000, on_prem: Optional[bool] = None
    ) -> list:
        """
        Fetches insights results.

        This function fetches insights results using the specified parameters.

        Args:
            insight_id (str): The ID of the insight.
            count (int): The number of results to fetch.

        Returns:
            dict: A dictionary containing the fetched insight results.

        Example:
            # Instantiate BruceHandler
            >>> bruce_handler = BruceHandler(data_url="example.com", user_id="userID")
            # Example
            >>> insight_id = "insightID"
            >>> fetched_results = bruce_handler.fetch_insight_results(insight_id=insight_id)
            # Example
            >>> count = num
            >>> insight_id = "insightID"
            >>> fetched_results = bruce_handler.fetch_insight_results(insight_id=insight_id, count=count)

        """
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.GET_INSIGHT_RESULT.format(
                protocol=protocol, data_url=self.data_url, count=count
            )

            # Prepare the request payload
            payload = {"insightID": insight_id}

            # Send the request via HTTP PUT with headers
            response = requests.put(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            response_data = json.loads(response.text)

            if not response_data["success"]:
                raise ValueError(response_data)

            return response_data["data"]

        except (TypeError, ValueError, requests.exceptions.RequestException) as e:
            print(f"[EXCEPTION] {type(e).__name__}: {e}")
            return list

        except Exception as e:
            print(f"[EXCEPTION] {e}")
            return list

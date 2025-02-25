import requests
from typing import List, Dict, Tuple
import numpy as np
import imaging_server_kit as serverkit
from imaging_server_kit.errors import (
    AlgorithmNotFoundError,
    AlgorithmServerError,
    InvalidAlgorithmParametersError,
    ServerRequestError,
    AlgorithmTimeoutError,
)


class Client:
    def __init__(self, server_url: str = "") -> None:
        self._server_url = server_url
        self._algorithms = {}
        if server_url != "":
            self.connect(server_url)

    def connect(self, server_url: str) -> None:
        self.server_url = server_url
        endpoint = f"{self.server_url}/services"
        try:
            response = requests.get(endpoint)
        except requests.exceptions.RequestException as e:
            raise ServerRequestError(endpoint, e)

        if response.status_code == 200:
            services = response.json().get("services")
            self.algorithms = services
        else:
            raise AlgorithmServerError(response.status_code, response.text)

    @property
    def server_url(self) -> str:
        return self._server_url

    @server_url.setter
    def server_url(self, server_url: str):
        self._server_url = server_url

    @property
    def algorithms(self) -> Dict[str, str]:
        return self._algorithms

    @algorithms.setter
    def algorithms(self, algorithms: Dict[str, str]):
        self._algorithms = algorithms

    def run_algorithm(self, algorithm=None, **algo_params) -> List[Tuple]:
        algorithm = self._validate_algorithm(algorithm)
        algo_params_encoded = self._encode_numpy_parameters(algo_params)

        try:
            endpoint = f"{self.server_url}/{algorithm}/process"
            response = requests.post(
                endpoint,
                json=algo_params_encoded,
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                },
            )
        except requests.exceptions.RequestException as e:
            raise ServerRequestError(endpoint, e)

        if response.status_code == 201:
            return serverkit.deserialize_result_tuple(response.json())
        elif response.status_code == 422:
            raise InvalidAlgorithmParametersError(response.status_code, response.json())
        elif response.status_code == 504:
            raise AlgorithmTimeoutError(response.status_code, response.text)
        else:
            raise AlgorithmServerError(response.status_code, response.text)

    def get_algorithm_parameters(self, algorithm=None) -> Dict:
        algorithm = self._validate_algorithm(algorithm)

        endpoint = f"{self.server_url}/{algorithm}/parameters"

        try:
            response = requests.get(endpoint)
        except requests.exceptions.RequestException as e:
            raise ServerRequestError(endpoint, e)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise AlgorithmServerError(response.status_code, response.text)

    def get_sample_images(
        self, algorithm=None, first_only: bool = False
    ) -> List["np.ndarray"]:
        algorithm = self._validate_algorithm(algorithm)

        endpoint = f"{self.server_url}/{algorithm}/sample_images"
        
        try:
            response = requests.get(endpoint)
        except requests.exceptions.RequestException as e:
            raise ServerRequestError(endpoint, e)

        if response.status_code == 200:
            images = []
            for content in response.json().get("sample_images"):
                encoded_image = content.get("sample_image")
                image = serverkit.decode_contents(encoded_image)
                images.append(image)
                if first_only:
                    return image
            return images
        else:
            print(
                f"Error status while attempting to get algorithm sample images: {response.status_code}"
            )
            return -1

    def _validate_algorithm(self, algorithm=None) -> str:
        if algorithm is None:
            if len(self.algorithms) > 0:
                algorithm = self.algorithms[0]
            else:
                raise AlgorithmNotFoundError(algorithm)
        else:
            if algorithm not in self.algorithms:
                raise AlgorithmNotFoundError(algorithm)
        return algorithm

    def _encode_numpy_parameters(self, algo_params: dict) -> dict:
        for param in algo_params:
            if isinstance(algo_params[param], np.ndarray):
                algo_params[param] = serverkit.encode_contents(algo_params[param])
        return algo_params

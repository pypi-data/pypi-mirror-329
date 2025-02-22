import httpx


class InfuzuAPIError(Exception):
    def __init__(self, base_error: httpx.HTTPError) -> None:
        super().__init__(f"HTTP Error: {str(base_error)}")

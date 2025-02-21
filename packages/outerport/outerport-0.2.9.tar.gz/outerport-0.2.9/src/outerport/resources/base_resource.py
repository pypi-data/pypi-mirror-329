from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from outerport.client import OuterportClient


class BaseResource:
    def __init__(self, client: "OuterportClient") -> None:
        self.client = client

from uuid import uuid4
from typing import Optional

class Guest:

    def __init__(
        self,name: str,contact_info: str,guest_id: Optional[str] = None
        ):
        self._guest_id     = guest_id or uuid4().hex[:8]
        self._name         = name
        self._contact_info = contact_info

    @property
    def guest_id(self) -> str:
        return self._guest_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact_info(self) -> str:
        return self._contact_info

    def to_dict(self) -> dict:
        return {
            "Guest ID":      self._guest_id,
            "Name":          self._name,
            "Contact Info":  self._contact_info
        }

    def __str__(self) -> str:
        return f"Guest[{self._guest_id}] {self._name}"

    def __repr__(self) -> str:
        return str(self)

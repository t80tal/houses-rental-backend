from typing import List, Optional
from fastapi import Request


class HouseCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.price: Optional[int] = None
        self.address: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.price = form.get("price")
        self.address = form.get("address")
        self.description = form.get("description")

    def is_valid(self):

        if not self.title or not len(self.title) >= 4:
            self.errors.append("Title too short.")
        if not self.address or not len(self.address) >= 1:
            self.errors.append("A valid address is required")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description too short")
        try:
            self.price = int(self.price)
            if not self.price or self.price < 100:
                self.errors.append("Price must be above 100")
        except:
            self.errors.append("Type a valid price (only with numbers).")
        if not self.errors:
            return True
        return False

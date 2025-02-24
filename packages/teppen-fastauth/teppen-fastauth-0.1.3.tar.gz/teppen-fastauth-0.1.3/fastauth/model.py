from pydantic import BaseModel, RootModel
from typing import Optional, List


class AccessTokenPayload(BaseModel):
    id: int
    employee_num: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    phs_number: Optional[str]
    email: str
    validated: bool
    is_admin: bool
    initialized: bool
    organization_id: Optional[int]
    organization_name: Optional[str]
    organization_full_name: Optional[str]
    iss: str
    aud: str
    iat: int
    exp: int


class UserBase(BaseModel):
    id: int
    employee_num: str
    last_name: str
    first_name: str
    phs_number: str


class User(BaseModel):
    id: int
    email: str
    employee_num: str
    name: str
    last_name: str
    first_name: str
    phs_number: str
    is_admin: bool
    organization_id: Optional[int] = None
    organization_name: Optional[str] = None


class Users(RootModel[List[User]]):
    def __iter__(self):
        return self.root.__iter__()

    def __getitem__(self, item):
        return self.root.__getitem__(item)

    def __len__(self):
        return self.root.__len__()

    def __contains__(self, item):
        return self.root.__contains__(item)


class Organization(BaseModel):
    id: int
    name: str
    parent: Optional[int] = None


class OrganizationDetail(Organization):
    users: List[UserBase]


class Organizations(RootModel[List[Organization]]):
    def __iter__(self):
        return self.root.__iter__()

    def __getitem__(self, item):
        return self.root.__getitem__(item)

    def __len__(self):
        return self.root.__len__()

    def __contains__(self, item):
        return self.root.__contains__(item)

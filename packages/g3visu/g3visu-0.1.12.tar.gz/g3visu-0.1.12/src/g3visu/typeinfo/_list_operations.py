import typing

from pydantic import BaseModel


T = typing.TypeVar('T', bound=BaseModel)


class ListOperations(typing.Generic[T]):
    def __init__(self, data: list[T]) -> None:
        self.data: list[T] = data

    def get(self, item_name: str) -> T:
        for item in self.data:
            if not isinstance(item, BaseModel):
                continue
            if getattr(item, 'name', None) == item_name:
                return item
        raise KeyError(item_name)

    def add(
        self,
        item_name: str,
        item_data: T,
        raise_if_exists: bool = False,
        replace_if_exists: bool = False
    ) -> None:
        try:  # check if the item is already present in the list
            self.get(item_name)
            if raise_if_exists:
                raise ValueError(f'Item "{item_name}" already exists.')
            if replace_if_exists:
                self.delete(item_name)
        except KeyError:
            pass
        self.data.append(item_data)

    def delete(self, item_name: str) -> None:
        for item in self.data:
            if not isinstance(item, BaseModel):
                continue
            if getattr(item, 'name', None) == item_name:
                self.data.remove(item)
                break

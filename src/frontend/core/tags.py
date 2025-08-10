from dataclasses import dataclass
from collections.abc import Sequence
from typing import overload, Iterator
from typing import Final

@dataclass(frozen=True)
class Ids(Sequence[str]):
    _values: tuple[str, ...]
    
    def __len__(self) -> int:
        return len(self._values)
    
    @overload
    def __getitem__(self, idx: int) -> str: ...
        
    @overload
    def __getitem__(self, idx: slice) -> tuple[str, ...]: ...
    
    def __getitem__(self, idx): 
        return self._values[idx]
    
    def __iter__(self) -> Iterator[str]:
        return iter(self._values)
  
# window names for all windows in the app
WINDOW_TAGS: Final[Ids] = Ids((
    "login_window",
    "sign_up_window",
    "home_window",
    "settings_window"
))

if __name__ == "__main__":
    import this
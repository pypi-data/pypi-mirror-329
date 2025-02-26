import typing
from dataclasses import dataclass



def _unpack_convert(v, t=typing.Any):
    if v == "_":
        return None
    elif v in ["T", "F"] and t is bool:
        return True if v == "T" else False
    elif t is int:
        return int(v)
    else:
        return str(v)


def _pack_convert(v):
    if isinstance(v, bool):
        return "T" if v else "F"
    elif v is None:
        return "_"
    else:
        return str(v)


@dataclass(slots=True, )
class CoolBackData:
    """
    example:
    ctchm/city/msk/F/DFSFSDHBSEDFSDSDFSD/2
    ctchm/op/save/F/DFSFSDHBSEDFSDSDFSD/2
    """
    msg_type: str | None = None
    btn_type: str | None = None
    btn_id: str | None = None
    value: str | None = None
    checked: bool = False
    corr_id: str | None = None
    version: int | None = 2
    
    
    @staticmethod
    def from_str(cbd: str):
        return CoolBackData().unpack(cbd)
    
    
    def unpack(self, cbd: str):
        l = cbd.split("/")
        self.checked = _unpack_convert(l[4], bool)
        self.version = _unpack_convert(l[6], int) or self.version
        
        l = list(map(_unpack_convert, l))
        self.msg_type, self.btn_type, self.btn_id, self.value, _, self.corr_id, _ = l
        
        return self
    
    
    def pack(self):
        target = [self.msg_type, self.btn_type, self.btn_id, self.value, self.checked, self.corr_id, self.version]
        target = [_pack_convert(v) for v in target]
        res = "/".join(target)
        assert len(res) <= 64
        return res

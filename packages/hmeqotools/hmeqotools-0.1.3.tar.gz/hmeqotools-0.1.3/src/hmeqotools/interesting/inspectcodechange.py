from __future__ import annotations

import hashlib
import inspect
import re
import types as _types

DEFAULT_SIZE = 1000


def get_frame_vc(frame: _types.FrameType, size=DEFAULT_SIZE) -> int:
    """Get the vc of frame."""
    return get_vc(inspect.getsource(frame), size)


def get_vc(s: str, size=DEFAULT_SIZE) -> int:
    """Get the vc of str."""
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % size


def force_vc(frame: inspect._SourceObjectType, size=DEFAULT_SIZE) -> int | None:
    """Force the vc of frame."""
    source = inspect.getsource(frame)
    match = re.search(r"(?<=%s\()\d+" % inspectcodechange.__name__, source)
    if match:
        start, end = match.span()
        code_p1, code_p2 = source[:start], source[end:]
        for i in range(size):
            new_code = code_p1 + str(i) + code_p2
            vc = get_vc(new_code)
            if vc == i:
                return i
    return None


def inspectcodechange(vc: int) -> bool:
    """Inspect current frame code change."""
    frame = inspect.getouterframes(inspect.currentframe())[1].frame
    frame_code = inspect.getsource(frame)
    return vc == get_vc(frame_code)


def main(n=10):
    if inspectcodechange(7):
        print("验证成功")
    else:
        print("验证失败, 我的代码被修改了")
        return 0  # 整个bug
    return 2**n


if __name__ == "__main__":
    print(f"vc: {force_vc(main)}")
    print(main())

# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack11l1_opy_ = 7
def bstack111l1ll_opy_ (bstack111l1l1_opy_):
    global bstack1lll1ll_opy_
    bstack1l1l1_opy_ = ord (bstack111l1l1_opy_ [-1])
    bstack11111ll_opy_ = bstack111l1l1_opy_ [:-1]
    bstack1ll1ll_opy_ = bstack1l1l1_opy_ % len (bstack11111ll_opy_)
    bstack1lllll1_opy_ = bstack11111ll_opy_ [:bstack1ll1ll_opy_] + bstack11111ll_opy_ [bstack1ll1ll_opy_:]
    if bstack11l11ll_opy_:
        bstack11ll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l11l1_opy_ + bstack1l1l1_opy_) % bstack11l1_opy_) for bstack1l11l1_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack11ll1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l11l1_opy_ + bstack1l1l1_opy_) % bstack11l1_opy_) for bstack1l11l1_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack11ll1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1111ll11_opy_ import get_logger
from bstack_utils.bstack1l1111ll1_opy_ import bstack1111lllll1_opy_
bstack1l1111ll1_opy_ = bstack1111lllll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l1111ll_opy_: Optional[str] = None):
    bstack111l1ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᗦ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack111l11lll1_opy_: str = bstack1l1111ll1_opy_.bstack111l11llll_opy_(label)
            start_mark: str = label + bstack111l1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᗧ")
            end_mark: str = label + bstack111l1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᗨ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1l1ll1_opy_.value:
                    bstack1l1111ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1111ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l1111ll_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = bstack111l11lll1_opy_ + bstack111l1ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᗩ")
                    end_mark: str = bstack111l11lll1_opy_ + bstack111l1ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᗪ")
                    bstack1l1111ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1111ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l1111ll_opy_)
            except Exception as e:
                bstack1l1111ll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l1111ll_opy_)
            return result
        return wrapper
    return decorator
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
from collections import deque
from bstack_utils.constants import *
class bstack11l11l11l_opy_:
    def __init__(self):
        self._1ll1l11l111_opy_ = deque()
        self._1ll1l111lll_opy_ = {}
        self._1ll1l11lll1_opy_ = False
    def bstack1ll1l1111ll_opy_(self, test_name, bstack1ll1l111ll1_opy_):
        bstack1ll1l11llll_opy_ = self._1ll1l111lll_opy_.get(test_name, {})
        return bstack1ll1l11llll_opy_.get(bstack1ll1l111ll1_opy_, 0)
    def bstack1ll1l111l1l_opy_(self, test_name, bstack1ll1l111ll1_opy_):
        bstack1ll1l11ll1l_opy_ = self.bstack1ll1l1111ll_opy_(test_name, bstack1ll1l111ll1_opy_)
        self.bstack1ll1l11ll11_opy_(test_name, bstack1ll1l111ll1_opy_)
        return bstack1ll1l11ll1l_opy_
    def bstack1ll1l11ll11_opy_(self, test_name, bstack1ll1l111ll1_opy_):
        if test_name not in self._1ll1l111lll_opy_:
            self._1ll1l111lll_opy_[test_name] = {}
        bstack1ll1l11llll_opy_ = self._1ll1l111lll_opy_[test_name]
        bstack1ll1l11ll1l_opy_ = bstack1ll1l11llll_opy_.get(bstack1ll1l111ll1_opy_, 0)
        bstack1ll1l11llll_opy_[bstack1ll1l111ll1_opy_] = bstack1ll1l11ll1l_opy_ + 1
    def bstack1l1l11l1l_opy_(self, bstack1ll1l11l1ll_opy_, bstack1ll1l11l11l_opy_):
        bstack1ll1l1l1111_opy_ = self.bstack1ll1l111l1l_opy_(bstack1ll1l11l1ll_opy_, bstack1ll1l11l11l_opy_)
        event_name = bstack11111lll1l_opy_[bstack1ll1l11l11l_opy_]
        bstack1ll1l11l1l1_opy_ = bstack111l1ll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᚥ").format(bstack1ll1l11l1ll_opy_, event_name, bstack1ll1l1l1111_opy_)
        self._1ll1l11l111_opy_.append(bstack1ll1l11l1l1_opy_)
    def bstack1lll1l111l_opy_(self):
        return len(self._1ll1l11l111_opy_) == 0
    def bstack11ll11lll1_opy_(self):
        bstack1ll1l111l11_opy_ = self._1ll1l11l111_opy_.popleft()
        return bstack1ll1l111l11_opy_
    def capturing(self):
        return self._1ll1l11lll1_opy_
    def bstack1ll1l1111l_opy_(self):
        self._1ll1l11lll1_opy_ = True
    def bstack111llll11_opy_(self):
        self._1ll1l11lll1_opy_ = False
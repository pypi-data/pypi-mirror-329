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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack111l1lll1l_opy_ as bstack1l1llll111_opy_
from browserstack_sdk.bstack1ll11ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1ll1ll_opy_
class bstack1l1l11ll1l_opy_:
    def __init__(self, args, logger, bstack111ll1l1ll_opy_, bstack111ll1111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        self.bstack111ll1111l_opy_ = bstack111ll1111l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll1lll1l_opy_ = []
        self.bstack111ll1ll11_opy_ = None
        self.bstack1l111l11l1_opy_ = []
        self.bstack111ll1l1l1_opy_ = self.bstack1l1llll1_opy_()
        self.bstack1l111lllll_opy_ = -1
    def bstack11ll11l1l1_opy_(self, bstack111l1lllll_opy_):
        self.parse_args()
        self.bstack111ll111l1_opy_()
        self.bstack111ll11ll1_opy_(bstack111l1lllll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111ll11l11_opy_():
        import importlib
        if getattr(importlib, bstack111l1ll_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪྍ"), False):
            bstack111l1llll1_opy_ = importlib.find_loader(bstack111l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨྎ"))
        else:
            bstack111l1llll1_opy_ = importlib.util.find_spec(bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩྏ"))
    def bstack111ll11111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l111lllll_opy_ = -1
        if self.bstack111ll1111l_opy_ and bstack111l1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨྐ") in self.bstack111ll1l1ll_opy_:
            self.bstack1l111lllll_opy_ = int(self.bstack111ll1l1ll_opy_[bstack111l1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩྑ")])
        try:
            bstack111ll1lll1_opy_ = [bstack111l1ll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬྒ"), bstack111l1ll_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧྒྷ"), bstack111l1ll_opy_ (u"ࠬ࠳ࡰࠨྔ")]
            if self.bstack1l111lllll_opy_ >= 0:
                bstack111ll1lll1_opy_.extend([bstack111l1ll_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧྕ"), bstack111l1ll_opy_ (u"ࠧ࠮ࡰࠪྖ")])
            for arg in bstack111ll1lll1_opy_:
                self.bstack111ll11111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111ll111l1_opy_(self):
        bstack111ll1ll11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111ll1ll11_opy_ = bstack111ll1ll11_opy_
        return bstack111ll1ll11_opy_
    def bstack1l11lll1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111ll11l11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1ll1ll_opy_)
    def bstack111ll11ll1_opy_(self, bstack111l1lllll_opy_):
        bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
        if bstack111l1lllll_opy_:
            self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬྗ"))
            self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠩࡗࡶࡺ࡫ࠧ྘"))
        if bstack1ll11lll_opy_.bstack111ll11l1l_opy_():
            self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩྙ"))
            self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"࡙ࠫࡸࡵࡦࠩྚ"))
        self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠬ࠳ࡰࠨྛ"))
        self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫྜ"))
        self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩྜྷ"))
        self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨྞ"))
        if self.bstack1l111lllll_opy_ > 1:
            self.bstack111ll1ll11_opy_.append(bstack111l1ll_opy_ (u"ࠩ࠰ࡲࠬྟ"))
            self.bstack111ll1ll11_opy_.append(str(self.bstack1l111lllll_opy_))
    def bstack111ll1l11l_opy_(self):
        bstack1l111l11l1_opy_ = []
        for spec in self.bstack11ll1lll1l_opy_:
            bstack1ll111llll_opy_ = [spec]
            bstack1ll111llll_opy_ += self.bstack111ll1ll11_opy_
            bstack1l111l11l1_opy_.append(bstack1ll111llll_opy_)
        self.bstack1l111l11l1_opy_ = bstack1l111l11l1_opy_
        return bstack1l111l11l1_opy_
    def bstack1l1llll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111ll1l1l1_opy_ = True
            return True
        except Exception as e:
            self.bstack111ll1l1l1_opy_ = False
        return self.bstack111ll1l1l1_opy_
    def bstack1ll11l1l1_opy_(self, bstack111ll11lll_opy_, bstack11ll11l1l1_opy_):
        bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪྠ")] = self.bstack111ll1l1ll_opy_
        multiprocessing.set_start_method(bstack111l1ll_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪྡ"))
        bstack1l11l11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l11l1l1l_opy_ = manager.list()
        if bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྡྷ") in self.bstack111ll1l1ll_opy_:
            for index, platform in enumerate(self.bstack111ll1l1ll_opy_[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩྣ")]):
                bstack1l11l11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111ll11lll_opy_,
                                                            args=(self.bstack111ll1ll11_opy_, bstack11ll11l1l1_opy_, bstack1l11l1l1l_opy_)))
            bstack111ll1ll1l_opy_ = len(self.bstack111ll1l1ll_opy_[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪྤ")])
        else:
            bstack1l11l11l11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111ll11lll_opy_,
                                                        args=(self.bstack111ll1ll11_opy_, bstack11ll11l1l1_opy_, bstack1l11l1l1l_opy_)))
            bstack111ll1ll1l_opy_ = 1
        i = 0
        for t in bstack1l11l11l11_opy_:
            os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨྥ")] = str(i)
            if bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬྦ") in self.bstack111ll1l1ll_opy_:
                os.environ[bstack111l1ll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫྦྷ")] = json.dumps(self.bstack111ll1l1ll_opy_[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧྨ")][i % bstack111ll1ll1l_opy_])
            i += 1
            t.start()
        for t in bstack1l11l11l11_opy_:
            t.join()
        return list(bstack1l11l1l1l_opy_)
    @staticmethod
    def bstack1l111l1ll1_opy_(driver, bstack111ll1l111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩྩ"), None)
        if item and getattr(item, bstack111l1ll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨྪ"), None) and not getattr(item, bstack111l1ll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩྫ"), False):
            logger.info(
                bstack111l1ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢྫྷ"))
            bstack111ll111ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1llll111_opy_.bstack11lll1l1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
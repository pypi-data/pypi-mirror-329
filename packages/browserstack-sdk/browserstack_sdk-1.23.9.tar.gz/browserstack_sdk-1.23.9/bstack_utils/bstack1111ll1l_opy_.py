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
class bstack1ll1l111_opy_:
    def __init__(self, handler):
        self._1ll111ll1l1_opy_ = None
        self.handler = handler
        self._1ll111ll11l_opy_ = self.bstack1ll111ll111_opy_()
        self.patch()
    def patch(self):
        self._1ll111ll1l1_opy_ = self._1ll111ll11l_opy_.execute
        self._1ll111ll11l_opy_.execute = self.bstack1ll111ll1ll_opy_()
    def bstack1ll111ll1ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᜓ"), driver_command, None, this, args)
            response = self._1ll111ll1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l1ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ᜔"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll111ll11l_opy_.execute = self._1ll111ll1l1_opy_
    @staticmethod
    def bstack1ll111ll111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
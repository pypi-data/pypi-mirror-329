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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack111ll1l1ll_opy_, bstack111ll1111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        self.bstack111ll1111l_opy_ = bstack111ll1111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111ll1llll_opy_(bstack111l1ll1l1_opy_):
        bstack111l1ll1ll_opy_ = []
        if bstack111l1ll1l1_opy_:
            tokens = str(os.path.basename(bstack111l1ll1l1_opy_)).split(bstack111l1ll_opy_ (u"ࠤࡢࠦྭ"))
            camelcase_name = bstack111l1ll_opy_ (u"ࠥࠤࠧྮ").join(t.title() for t in tokens)
            suite_name, bstack111l1ll11l_opy_ = os.path.splitext(camelcase_name)
            bstack111l1ll1ll_opy_.append(suite_name)
        return bstack111l1ll1ll_opy_
    @staticmethod
    def bstack111l1lll11_opy_(typename):
        if bstack111l1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢྯ") in typename:
            return bstack111l1ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨྰ")
        return bstack111l1ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢྱ")
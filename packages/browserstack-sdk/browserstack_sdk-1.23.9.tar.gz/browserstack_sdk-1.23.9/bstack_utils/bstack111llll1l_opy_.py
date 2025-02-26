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
from browserstack_sdk.bstack1l1l1l1111_opy_ import bstack1l1l11ll1l_opy_
from browserstack_sdk.bstack11l11ll1ll_opy_ import RobotHandler
def bstack1lllllll1_opy_(framework):
    if framework.lower() == bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᎛"):
        return bstack1l1l11ll1l_opy_.version()
    elif framework.lower() == bstack111l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ᎜"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ᎝"):
        import behave
        return behave.__version__
    else:
        return bstack111l1ll_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫ᎞")
def bstack1l1ll11111_opy_():
    import bstack111111l11l_opy_
    framework_name=[]
    bstack1111111lll_opy_=[]
    try:
        from selenium import webdriver
        framework_name.append(bstack111l1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭᎟"))
        bstack1111111lll_opy_.append(bstack111111l11l_opy_.bstack111111l111_opy_(bstack111l1ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᎠ")).version)
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᎡ"))
        bstack1111111lll_opy_.append(bstack111111l11l_opy_.bstack111111l111_opy_(bstack111l1ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᎢ")).version)
    except:
        pass
    return {
        bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꭳ"): bstack111l1ll_opy_ (u"ࠩࡢࠫᎤ").join(framework_name),
        bstack111l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᎥ"): bstack111l1ll_opy_ (u"ࠫࡤ࠭Ꭶ").join(bstack1111111lll_opy_)
    }
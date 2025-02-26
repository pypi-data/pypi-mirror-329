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
import threading
import logging
import bstack_utils.bstack111l1lll1l_opy_ as bstack1l1llll111_opy_
from bstack_utils.helper import bstack11llll11l_opy_
logger = logging.getLogger(__name__)
def bstack111l11ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1ll1l11111_opy_(context, *args):
    tags = getattr(args[0], bstack111l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬၽ"), [])
    bstack11lll1111_opy_ = bstack1l1llll111_opy_.bstack1llll1ll1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack11lll1111_opy_
    try:
      bstack1l1llllll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll1_opy_(bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧၾ")) else context.browser
      if bstack1l1llllll1_opy_ and bstack1l1llllll1_opy_.session_id and bstack11lll1111_opy_ and bstack11llll11l_opy_(
              threading.current_thread(), bstack111l1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨၿ"), None):
          threading.current_thread().isA11yTest = bstack1l1llll111_opy_.bstack11ll111l1_opy_(bstack1l1llllll1_opy_, bstack11lll1111_opy_)
    except Exception as e:
       logger.debug(bstack111l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪႀ").format(str(e)))
def bstack11l1l1l1l_opy_(bstack1l1llllll1_opy_):
    if bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨႁ"), None) and bstack11llll11l_opy_(
      threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫႂ"), None) and not bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩႃ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1llll111_opy_.bstack11lll1l1l1_opy_(bstack1l1llllll1_opy_, name=bstack111l1ll_opy_ (u"ࠢࠣႄ"), path=bstack111l1ll_opy_ (u"ࠣࠤႅ"))
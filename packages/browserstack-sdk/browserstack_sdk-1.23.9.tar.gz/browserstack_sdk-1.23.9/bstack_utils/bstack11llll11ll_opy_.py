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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111l11111l_opy_, bstack1ll1l1l1_opy_, get_host_info, bstack1lll1lll1ll_opy_, \
 bstack1llllll11_opy_, bstack11llll11l_opy_, bstack11l1111l11_opy_, bstack1llll1111l1_opy_, bstack1ll111l1l_opy_
import bstack_utils.bstack111l1lll1l_opy_ as bstack1l1llll111_opy_
from bstack_utils.bstack11l1ll11l1_opy_ import bstack11l111ll1_opy_
from bstack_utils.percy import bstack1llll111_opy_
from bstack_utils.config import Config
bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llll111_opy_()
@bstack11l1111l11_opy_(class_method=False)
def bstack1l1llllll11_opy_(bs_config, bstack1llll1ll1_opy_):
  try:
    data = {
        bstack111l1ll_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᢄ"): bstack111l1ll_opy_ (u"ࠬࡰࡳࡰࡰࠪᢅ"),
        bstack111l1ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᢆ"): bs_config.get(bstack111l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᢇ"), bstack111l1ll_opy_ (u"ࠨࠩᢈ")),
        bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢉ"): bs_config.get(bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᢊ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢋ"): bs_config.get(bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢌ")),
        bstack111l1ll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᢍ"): bs_config.get(bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᢎ"), bstack111l1ll_opy_ (u"ࠨࠩᢏ")),
        bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᢐ"): bstack1ll111l1l_opy_(),
        bstack111l1ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢑ"): bstack1lll1lll1ll_opy_(bs_config),
        bstack111l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᢒ"): get_host_info(),
        bstack111l1ll_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᢓ"): bstack1ll1l1l1_opy_(),
        bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᢔ"): os.environ.get(bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᢕ")),
        bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᢖ"): os.environ.get(bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᢗ"), False),
        bstack111l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᢘ"): bstack111l11111l_opy_(),
        bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᢙ"): bstack1l1ll1lllll_opy_(),
        bstack111l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩᢚ"): bstack1l1ll1ll1ll_opy_(bstack1llll1ll1_opy_),
        bstack111l1ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᢛ"): bstack1l111l1ll_opy_(bs_config, bstack1llll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᢜ"), bstack111l1ll_opy_ (u"ࠨࠩᢝ"))),
        bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᢞ"): bstack1llllll11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111l1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦᢟ").format(str(error)))
    return None
def bstack1l1ll1ll1ll_opy_(framework):
  return {
    bstack111l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᢠ"): framework.get(bstack111l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᢡ"), bstack111l1ll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᢢ")),
    bstack111l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᢣ"): framework.get(bstack111l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᢤ")),
    bstack111l1ll_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᢥ"): framework.get(bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᢦ")),
    bstack111l1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᢧ"): bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᢨ"),
    bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰᢩ࠭"): framework.get(bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᢪ"))
  }
def bstack1l111l1ll_opy_(bs_config, framework):
  bstack1l1llll1l1_opy_ = False
  bstack1ll111l111_opy_ = False
  bstack1l1ll1lll1l_opy_ = False
  if bstack111l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᢫") in bs_config:
    bstack1l1ll1lll1l_opy_ = True
  elif bstack111l1ll_opy_ (u"ࠩࡤࡴࡵ࠭᢬") in bs_config:
    bstack1l1llll1l1_opy_ = True
  else:
    bstack1ll111l111_opy_ = True
  bstack1l11ll1ll_opy_ = {
    bstack111l1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᢭"): bstack11l111ll1_opy_.bstack1l1ll1llll1_opy_(bs_config, framework),
    bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᢮"): bstack1l1llll111_opy_.bstack111l11ll1l_opy_(bs_config),
    bstack111l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᢯"): bs_config.get(bstack111l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᢰ"), False),
    bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᢱ"): bstack1ll111l111_opy_,
    bstack111l1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᢲ"): bstack1l1llll1l1_opy_,
    bstack111l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᢳ"): bstack1l1ll1lll1l_opy_
  }
  return bstack1l11ll1ll_opy_
@bstack11l1111l11_opy_(class_method=False)
def bstack1l1ll1lllll_opy_():
  try:
    bstack1l1ll1ll11l_opy_ = json.loads(os.getenv(bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᢴ"), bstack111l1ll_opy_ (u"ࠫࢀࢃࠧᢵ")))
    return {
        bstack111l1ll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᢶ"): bstack1l1ll1ll11l_opy_
    }
  except Exception as error:
    logger.error(bstack111l1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧᢷ").format(str(error)))
    return {}
def bstack1l1lll1l11l_opy_(array, bstack1l1ll1lll11_opy_, bstack1l1lll11111_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1ll1lll11_opy_]
    result[key] = o[bstack1l1lll11111_opy_]
  return result
def bstack1l1lll11l1l_opy_(bstack1l11111lll_opy_=bstack111l1ll_opy_ (u"ࠧࠨᢸ")):
  bstack1l1ll1ll1l1_opy_ = bstack1l1llll111_opy_.on()
  bstack1l1ll1l1lll_opy_ = bstack11l111ll1_opy_.on()
  bstack1l1lll1111l_opy_ = percy.bstack1l1l111ll1_opy_()
  if bstack1l1lll1111l_opy_ and not bstack1l1ll1l1lll_opy_ and not bstack1l1ll1ll1l1_opy_:
    return bstack1l11111lll_opy_ not in [bstack111l1ll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᢹ"), bstack111l1ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᢺ")]
  elif bstack1l1ll1ll1l1_opy_ and not bstack1l1ll1l1lll_opy_:
    return bstack1l11111lll_opy_ not in [bstack111l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᢻ"), bstack111l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᢼ"), bstack111l1ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᢽ")]
  return bstack1l1ll1ll1l1_opy_ or bstack1l1ll1l1lll_opy_ or bstack1l1lll1111l_opy_
@bstack11l1111l11_opy_(class_method=False)
def bstack1l1llll11ll_opy_(bstack1l11111lll_opy_, test=None):
  bstack1l1ll1ll111_opy_ = bstack1l1llll111_opy_.on()
  if not bstack1l1ll1ll111_opy_ or bstack1l11111lll_opy_ not in [bstack111l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᢾ")] or test == None:
    return None
  return {
    bstack111l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᢿ"): bstack1l1ll1ll111_opy_ and bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᣀ"), None) == True and bstack1l1llll111_opy_.bstack1llll1ll1l_opy_(test[bstack111l1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᣁ")])
  }
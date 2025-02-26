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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.measure import bstack1l1111ll1_opy_
from bstack_utils.percy import *
from browserstack_sdk.bstack11ll1l11_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll1ll11_opy_ import bstack11l11l11l_opy_
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1llll1l11l_opy_():
  global CONFIG
  headers = {
        bstack111l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1111l1l1_opy_(CONFIG, bstack1llll11l1_opy_)
  try:
    response = requests.get(bstack1llll11l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11l11lll_opy_ = response.json()[bstack111l1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lllll11l1_opy_.format(response.json()))
      return bstack1l11l11lll_opy_
    else:
      logger.debug(bstack1lll11l1_opy_.format(bstack111l1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lll11l1_opy_.format(e))
def bstack1lllll1111_opy_(hub_url):
  global CONFIG
  url = bstack111l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1111l1l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11llllll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111ll1l1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11llll111l_opy_, stage=STAGE.SINGLE)
def bstack11lll1ll11_opy_():
  try:
    global bstack1lll11l111_opy_
    bstack1l11l11lll_opy_ = bstack1llll1l11l_opy_()
    bstack1ll1lll11_opy_ = []
    results = []
    for bstack1l1lllll1_opy_ in bstack1l11l11lll_opy_:
      bstack1ll1lll11_opy_.append(bstack1ll1ll1ll_opy_(target=bstack1lllll1111_opy_,args=(bstack1l1lllll1_opy_,)))
    for t in bstack1ll1lll11_opy_:
      t.start()
    for t in bstack1ll1lll11_opy_:
      results.append(t.join())
    bstack11l11l1l1_opy_ = {}
    for item in results:
      hub_url = item[bstack111l1ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l1ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l11l1l1_opy_[hub_url] = latency
    bstack1l11lllll_opy_ = min(bstack11l11l1l1_opy_, key= lambda x: bstack11l11l1l1_opy_[x])
    bstack1lll11l111_opy_ = bstack1l11lllll_opy_
    logger.debug(bstack1lll1l1111_opy_.format(bstack1l11lllll_opy_))
  except Exception as e:
    logger.debug(bstack11l11lll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1111ll11_opy_
from bstack_utils.helper import bstack111l11ll_opy_, bstack11ll1111_opy_, bstack1lll111l11_opy_, bstack11llll11l_opy_, \
  bstack1llllll11_opy_, \
  Notset, bstack1l111lll1_opy_, \
  bstack1l111ll11_opy_, bstack1l11ll11_opy_, bstack1l11l111l_opy_, bstack1ll1l1l1_opy_, bstack1l11l11ll1_opy_, bstack1l11ll1l_opy_, \
  bstack11ll1ll1ll_opy_, \
  bstack1lll1l11ll_opy_, bstack11ll1ll1l1_opy_, bstack1ll1l1lll_opy_, bstack11111l1l1_opy_, \
  bstack1l1ll111_opy_, bstack1ll11111_opy_, bstack1l1111111_opy_, bstack1l1ll1l111_opy_
from bstack_utils.bstack111llll1l_opy_ import bstack1lllllll1_opy_, bstack1l1ll11111_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack1ll1l111_opy_
from bstack_utils.bstack1l11l1lll1_opy_ import bstack11l1lllll1_opy_, bstack11ll111l11_opy_
from bstack_utils.bstack1l1111l111_opy_ import bstack1l1111l111_opy_
from bstack_utils.proxy import bstack1111llll1_opy_, bstack1111l1l1_opy_, bstack1ll1111111_opy_, bstack1lll1ll1l1_opy_
from browserstack_sdk.bstack1l1l1l1111_opy_ import *
from browserstack_sdk.bstack1ll11ll1_opy_ import *
from bstack_utils.bstack111111l11_opy_ import bstack111l11111_opy_
from browserstack_sdk.bstack1l1111l11l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1111ll11_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1ll1l1lll1_opy_, stage=STAGE.SINGLE)
def bstack1llll1l1l_opy_():
    global bstack1lll11l111_opy_
    try:
        bstack1l111l111_opy_ = bstack1l1ll1l1l1_opy_()
        bstack11l1ll11l_opy_(bstack1l111l111_opy_)
        hub_url = bstack1l111l111_opy_.get(bstack111l1ll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack111l1ll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack111l1ll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack111l1ll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1lll11l111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1ll1l1l1_opy_():
    global CONFIG
    bstack11llll1ll_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack111l1ll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack111l1ll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11llll1ll_opy_, str):
        raise ValueError(bstack111l1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l111l111_opy_ = bstack1l111ll1_opy_(bstack11llll1ll_opy_)
        return bstack1l111l111_opy_
    except Exception as e:
        logger.error(bstack111l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1l111ll1_opy_(bstack11llll1ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack111l1ll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l1ll11l11_opy_ + bstack11llll1ll_opy_
        auth = (CONFIG[bstack111l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack111l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11lll11ll1_opy_ = json.loads(response.text)
            return bstack11lll11ll1_opy_
    except ValueError as ve:
        logger.error(bstack111l1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11l1ll11l_opy_(bstack1l1l11ll_opy_):
    global CONFIG
    if bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack111l1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack111l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack111l1ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1l1l11ll_opy_:
        bstack1lll1l11l1_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack111l1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1lll1l11l1_opy_)
        bstack1lll1ll11l_opy_ = bstack1l1l11ll_opy_.get(bstack111l1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1l1ll11l1l_opy_ = bstack111l1ll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1lll1ll11l_opy_)
        logger.debug(bstack111l1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1l1ll11l1l_opy_)
        bstack111l111ll_opy_ = {
            bstack111l1ll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack111l1ll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack111l1ll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack111l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack111l1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1l1ll11l1l_opy_
        }
        bstack1lll1l11l1_opy_.update(bstack111l111ll_opy_)
        logger.debug(bstack111l1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1lll1l11l1_opy_)
        CONFIG[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1lll1l11l1_opy_
        logger.debug(bstack111l1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1l1111llll_opy_():
    bstack1l111l111_opy_ = bstack1l1ll1l1l1_opy_()
    if not bstack1l111l111_opy_[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack111l1ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l111l111_opy_[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack111l1ll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11111l111_opy_, stage=STAGE.SINGLE)
def bstack1l1lll1l11_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l11l1111_opy_
        logger.debug(bstack111l1ll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111l1ll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack111l1ll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1ll1lll1l_opy_ = json.loads(response.text)
                bstack1lllll111_opy_ = bstack1ll1lll1l_opy_.get(bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1lllll111_opy_:
                    bstack1l1l1ll1ll_opy_ = bstack1lllll111_opy_[0]
                    bstack11lllll11_opy_ = bstack1l1l1ll1ll_opy_.get(bstack111l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack111ll1l11_opy_ = bstack1ll1ll1l1l_opy_ + bstack11lllll11_opy_
                    result.extend([bstack11lllll11_opy_, bstack111ll1l11_opy_])
                    logger.info(bstack1l1ll1lll_opy_.format(bstack111ll1l11_opy_))
                    bstack11l11ll1_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack11l11ll1_opy_ += bstack111l1ll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack11l11ll1_opy_ != bstack1l1l1ll1ll_opy_.get(bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l11lllll1_opy_.format(bstack1l1l1ll1ll_opy_.get(bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack11l11ll1_opy_))
                    return result
                else:
                    logger.debug(bstack111l1ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack111l1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack111l1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack111l1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack11llll11ll_opy_ as bstack1l111l1lll_opy_
import bstack_utils.bstack111l11l1_opy_ as bstack11ll1111ll_opy_
bstack1l1ll11ll1_opy_ = bstack111l1ll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࢹ")
bstack11l1ll11_opy_ = bstack111l1ll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࢺ")
from ._version import __version__
bstack1111l1111_opy_ = None
CONFIG = {}
bstack1l11l11l1l_opy_ = {}
bstack1ll1lll1_opy_ = {}
bstack11ll1111l1_opy_ = None
bstack11l111l1l_opy_ = None
bstack1ll1l1ll1l_opy_ = None
bstack1ll11l11l_opy_ = -1
bstack1lll1l1ll_opy_ = 0
bstack1l111ll111_opy_ = bstack1lll1ll11_opy_
bstack1ll11lll1l_opy_ = 1
bstack111lll1ll_opy_ = False
bstack1ll11l1l11_opy_ = False
bstack11ll1l1lll_opy_ = bstack111l1ll_opy_ (u"ࠩࠪࢻ")
bstack1l1ll1l11l_opy_ = bstack111l1ll_opy_ (u"ࠪࠫࢼ")
bstack11l11l1l_opy_ = False
bstack1ll1ll11l_opy_ = True
bstack1ll111l1ll_opy_ = bstack111l1ll_opy_ (u"ࠫࠬࢽ")
bstack1ll1ll11ll_opy_ = []
bstack1lll11l111_opy_ = bstack111l1ll_opy_ (u"ࠬ࠭ࢾ")
bstack1l111l1l11_opy_ = False
bstack1ll1l111l1_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack11lll1ll_opy_ = None
bstack1lll1111l_opy_ = -1
bstack1ll1ll111_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"࠭ࡾࠨࢿ")), bstack111l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣀ"), bstack111l1ll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣁ"))
bstack1l1111l1ll_opy_ = 0
bstack1l1l1l111_opy_ = 0
bstack11lll11l_opy_ = []
bstack1ll1llll_opy_ = []
bstack1l1l111l1l_opy_ = []
bstack1ll1llllll_opy_ = []
bstack1ll11l11_opy_ = bstack111l1ll_opy_ (u"ࠩࠪࣂ")
bstack1l1ll1111l_opy_ = bstack111l1ll_opy_ (u"ࠪࠫࣃ")
bstack1ll11l1l1l_opy_ = False
bstack1llll111l1_opy_ = False
bstack11ll1ll11l_opy_ = {}
bstack1ll111ll_opy_ = None
bstack1lllll11ll_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1l1111ll_opy_ = None
bstack1l11ll1l1_opy_ = None
bstack1lll1l111_opy_ = None
bstack11ll1lll1_opy_ = None
bstack1l111l11ll_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack11llll1l1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1l1llllll_opy_ = None
bstack1l11111111_opy_ = None
bstack1l11ll11l_opy_ = None
bstack1l1l1lll1_opy_ = None
bstack1ll11l111_opy_ = None
bstack1llll11ll_opy_ = None
bstack111l11l11_opy_ = None
bstack1llll1ll_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack1lll1l11l_opy_ = None
bstack111lllll_opy_ = None
bstack1ll11l11l1_opy_ = False
bstack11111lll1_opy_ = bstack111l1ll_opy_ (u"ࠦࠧࣄ")
logger = bstack1111ll11_opy_.get_logger(__name__, bstack1l111ll111_opy_)
bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
percy = bstack1llll111_opy_()
bstack11lllll1_opy_ = bstack11l11l11l_opy_()
bstack1l11l1l1_opy_ = bstack1l1111l11l_opy_()
def bstack11ll1l1ll1_opy_():
  global CONFIG
  global bstack1ll11l1l1l_opy_
  global bstack1ll11lll_opy_
  bstack1111l1l1l_opy_ = bstack1ll1l1l1ll_opy_(CONFIG)
  if bstack1llllll11_opy_(CONFIG):
    if (bstack111l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣅ") in bstack1111l1l1l_opy_ and str(bstack1111l1l1l_opy_[bstack111l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣆ")]).lower() == bstack111l1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬࣇ")):
      bstack1ll11l1l1l_opy_ = True
    bstack1ll11lll_opy_.bstack1ll1l1l1l_opy_(bstack1111l1l1l_opy_.get(bstack111l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣈ"), False))
  else:
    bstack1ll11l1l1l_opy_ = True
    bstack1ll11lll_opy_.bstack1ll1l1l1l_opy_(True)
def bstack111ll1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llll11lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1lllll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l1ll_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨࣉ") == args[i].lower() or bstack111l1ll_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦ࣊") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll111l1ll_opy_
      bstack1ll111l1ll_opy_ += bstack111l1ll_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ࣋") + path
      return path
  return None
bstack1l11ll111l_opy_ = re.compile(bstack111l1ll_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿ࠣ࣌"))
def bstack11lll1l1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11ll111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l1ll_opy_ (u"ࠨࠤࡼࠤ࣍") + group + bstack111l1ll_opy_ (u"ࠢࡾࠤ࣎"), os.environ.get(group))
  return value
def bstack1lllll111l_opy_():
  bstack1ll11l1ll_opy_ = bstack11ll1lllll_opy_()
  if bstack1ll11l1ll_opy_ and os.path.exists(os.path.abspath(bstack1ll11l1ll_opy_)):
    fileName = bstack1ll11l1ll_opy_
  if bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉ࣏ࠬ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࣐࠭")])) and not bstack111l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩ࣑ࠬ") in locals():
    fileName = os.environ[bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")]
  if bstack111l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࣓ࠧ") in locals():
    bstack1l11ll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11ll1_opy_ = bstack111l1ll_opy_ (u"࠭ࠧࣔ")
  bstack1llll1l11_opy_ = os.getcwd()
  bstack11l11ll11_opy_ = bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣕ")
  bstack111ll1ll_opy_ = bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣖ")
  while (not os.path.exists(bstack1l11ll1_opy_)) and bstack1llll1l11_opy_ != bstack111l1ll_opy_ (u"ࠤࠥࣗ"):
    bstack1l11ll1_opy_ = os.path.join(bstack1llll1l11_opy_, bstack11l11ll11_opy_)
    if not os.path.exists(bstack1l11ll1_opy_):
      bstack1l11ll1_opy_ = os.path.join(bstack1llll1l11_opy_, bstack111ll1ll_opy_)
    if bstack1llll1l11_opy_ != os.path.dirname(bstack1llll1l11_opy_):
      bstack1llll1l11_opy_ = os.path.dirname(bstack1llll1l11_opy_)
    else:
      bstack1llll1l11_opy_ = bstack111l1ll_opy_ (u"ࠥࠦࣘ")
  if not os.path.exists(bstack1l11ll1_opy_):
    bstack1ll1l111ll_opy_(
      bstack11111111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11ll1_opy_, bstack111l1ll_opy_ (u"ࠫࡷ࠭ࣙ")) as stream:
      yaml.add_implicit_resolver(bstack111l1ll_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣚ"), bstack1l11ll111l_opy_)
      yaml.add_constructor(bstack111l1ll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣛ"), bstack11lll1l1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l11ll1_opy_, bstack111l1ll_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1l111ll_opy_(bstack11l1111l_opy_.format(str(exc)))
def bstack1l1ll111ll_opy_(config):
  bstack1l1lll11l1_opy_ = bstack1lll1l1l_opy_(config)
  for option in list(bstack1l1lll11l1_opy_):
    if option.lower() in bstack11l1lllll_opy_ and option != bstack11l1lllll_opy_[option.lower()]:
      bstack1l1lll11l1_opy_[bstack11l1lllll_opy_[option.lower()]] = bstack1l1lll11l1_opy_[option]
      del bstack1l1lll11l1_opy_[option]
  return config
def bstack11llll1l11_opy_():
  global bstack1ll1lll1_opy_
  for key, bstack11ll11llll_opy_ in bstack1ll111111_opy_.items():
    if isinstance(bstack11ll11llll_opy_, list):
      for var in bstack11ll11llll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1lll1_opy_[key] = os.environ[var]
          break
    elif bstack11ll11llll_opy_ in os.environ and os.environ[bstack11ll11llll_opy_] and str(os.environ[bstack11ll11llll_opy_]).strip():
      bstack1ll1lll1_opy_[key] = os.environ[bstack11ll11llll_opy_]
  if bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣝ") in os.environ:
    bstack1ll1lll1_opy_[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ")] = {}
    bstack1ll1lll1_opy_[bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣟ")][bstack111l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")] = os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡")]
def bstack1l11lll11l_opy_():
  global bstack1l11l11l1l_opy_
  global bstack1ll111l1ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l1ll_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣢").lower() == val.lower():
      bstack1l11l11l1l_opy_[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")] = {}
      bstack1l11l11l1l_opy_[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣤ")][bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣥ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l111ll1l1_opy_ in bstack11111111_opy_.items():
    if isinstance(bstack1l111ll1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l111ll1l1_opy_:
          if idx < len(sys.argv) and bstack111l1ll_opy_ (u"ࠪ࠱࠲ࣦ࠭") + var.lower() == val.lower() and not key in bstack1l11l11l1l_opy_:
            bstack1l11l11l1l_opy_[key] = sys.argv[idx + 1]
            bstack1ll111l1ll_opy_ += bstack111l1ll_opy_ (u"ࠫࠥ࠳࠭ࠨࣧ") + var + bstack111l1ll_opy_ (u"ࠬࠦࠧࣨ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l1ll_opy_ (u"࠭࠭࠮ࣩࠩ") + bstack1l111ll1l1_opy_.lower() == val.lower() and not key in bstack1l11l11l1l_opy_:
          bstack1l11l11l1l_opy_[key] = sys.argv[idx + 1]
          bstack1ll111l1ll_opy_ += bstack111l1ll_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + bstack1l111ll1l1_opy_ + bstack111l1ll_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll11ll1l_opy_(config):
  bstack1l1l1ll1l_opy_ = config.keys()
  for bstack11lllll1l1_opy_, bstack11l1l111l_opy_ in bstack11lllll11l_opy_.items():
    if bstack11l1l111l_opy_ in bstack1l1l1ll1l_opy_:
      config[bstack11lllll1l1_opy_] = config[bstack11l1l111l_opy_]
      del config[bstack11l1l111l_opy_]
  for bstack11lllll1l1_opy_, bstack11l1l111l_opy_ in bstack1l1111l1l_opy_.items():
    if isinstance(bstack11l1l111l_opy_, list):
      for bstack1ll11llll_opy_ in bstack11l1l111l_opy_:
        if bstack1ll11llll_opy_ in bstack1l1l1ll1l_opy_:
          config[bstack11lllll1l1_opy_] = config[bstack1ll11llll_opy_]
          del config[bstack1ll11llll_opy_]
          break
    elif bstack11l1l111l_opy_ in bstack1l1l1ll1l_opy_:
      config[bstack11lllll1l1_opy_] = config[bstack11l1l111l_opy_]
      del config[bstack11l1l111l_opy_]
  for bstack1ll11llll_opy_ in list(config):
    for bstack1111lll11_opy_ in bstack11llll11l1_opy_:
      if bstack1ll11llll_opy_.lower() == bstack1111lll11_opy_.lower() and bstack1ll11llll_opy_ != bstack1111lll11_opy_:
        config[bstack1111lll11_opy_] = config[bstack1ll11llll_opy_]
        del config[bstack1ll11llll_opy_]
  bstack1llllll11l_opy_ = [{}]
  if not config.get(bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࣬")):
    config[bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࣭࠭")] = [{}]
  bstack1llllll11l_opy_ = config[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ࣮ࠧ")]
  for platform in bstack1llllll11l_opy_:
    for bstack1ll11llll_opy_ in list(platform):
      for bstack1111lll11_opy_ in bstack11llll11l1_opy_:
        if bstack1ll11llll_opy_.lower() == bstack1111lll11_opy_.lower() and bstack1ll11llll_opy_ != bstack1111lll11_opy_:
          platform[bstack1111lll11_opy_] = platform[bstack1ll11llll_opy_]
          del platform[bstack1ll11llll_opy_]
  for bstack11lllll1l1_opy_, bstack11l1l111l_opy_ in bstack1l1111l1l_opy_.items():
    for platform in bstack1llllll11l_opy_:
      if isinstance(bstack11l1l111l_opy_, list):
        for bstack1ll11llll_opy_ in bstack11l1l111l_opy_:
          if bstack1ll11llll_opy_ in platform:
            platform[bstack11lllll1l1_opy_] = platform[bstack1ll11llll_opy_]
            del platform[bstack1ll11llll_opy_]
            break
      elif bstack11l1l111l_opy_ in platform:
        platform[bstack11lllll1l1_opy_] = platform[bstack11l1l111l_opy_]
        del platform[bstack11l1l111l_opy_]
  for bstack1l1lll11_opy_ in bstack11lll11ll_opy_:
    if bstack1l1lll11_opy_ in config:
      if not bstack11lll11ll_opy_[bstack1l1lll11_opy_] in config:
        config[bstack11lll11ll_opy_[bstack1l1lll11_opy_]] = {}
      config[bstack11lll11ll_opy_[bstack1l1lll11_opy_]].update(config[bstack1l1lll11_opy_])
      del config[bstack1l1lll11_opy_]
  for platform in bstack1llllll11l_opy_:
    for bstack1l1lll11_opy_ in bstack11lll11ll_opy_:
      if bstack1l1lll11_opy_ in list(platform):
        if not bstack11lll11ll_opy_[bstack1l1lll11_opy_] in platform:
          platform[bstack11lll11ll_opy_[bstack1l1lll11_opy_]] = {}
        platform[bstack11lll11ll_opy_[bstack1l1lll11_opy_]].update(platform[bstack1l1lll11_opy_])
        del platform[bstack1l1lll11_opy_]
  config = bstack1l1ll111ll_opy_(config)
  return config
def bstack1l1111l1_opy_(config):
  global bstack1l1ll1l11l_opy_
  bstack1lll1ll1_opy_ = False
  if bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ࣯ࠩ") in config and str(config[bstack111l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࣰࠪ")]).lower() != bstack111l1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪࣱ࠭"):
    if bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࣲࠬ") not in config or str(config[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ࣳ")]).lower() == bstack111l1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
      config[bstack111l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࣵ")] = False
    else:
      bstack1l111l111_opy_ = bstack1l1ll1l1l1_opy_()
      if bstack111l1ll_opy_ (u"ࠬ࡯ࡳࡕࡴ࡬ࡥࡱࡍࡲࡪࡦࣶࠪ") in bstack1l111l111_opy_:
        if not bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣷ") in config:
          config[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣸ")] = {}
        config[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣹࠬ")][bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣺࠫ")] = bstack111l1ll_opy_ (u"ࠪࡥࡹࡹ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩࣻ")
        bstack1lll1ll1_opy_ = True
        bstack1l1ll1l11l_opy_ = config[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")].get(bstack111l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ"))
  if bstack1llllll11_opy_(config) and bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣾ") in config and str(config[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ")]).lower() != bstack111l1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ") and not bstack1lll1ll1_opy_:
    if not bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
      config[bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
    if not config[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")].get(bstack111l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩऄ")) and not bstack111l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨअ") in config[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")]:
      bstack1ll111l1l_opy_ = datetime.datetime.now()
      bstack1lllllll1l_opy_ = bstack1ll111l1l_opy_.strftime(bstack111l1ll_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬइ"))
      hostname = socket.gethostname()
      bstack1l111ll1l_opy_ = bstack111l1ll_opy_ (u"ࠩࠪई").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l1ll_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬउ").format(bstack1lllllll1l_opy_, hostname, bstack1l111ll1l_opy_)
      config[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")][bstack111l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऋ")] = identifier
    bstack1l1ll1l11l_opy_ = config[bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  return config
def bstack11llll1111_opy_():
  bstack11l1ll111_opy_ =  bstack1ll1l1l1_opy_()[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠧऎ")]
  return bstack11l1ll111_opy_ if bstack11l1ll111_opy_ else -1
def bstack1lll11llll_opy_(bstack11l1ll111_opy_):
  global CONFIG
  if not bstack111l1ll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫए") in CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ")]:
    return
  CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ")] = CONFIG[bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ")].replace(
    bstack111l1ll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ"),
    str(bstack11l1ll111_opy_)
  )
def bstack1l1l111ll_opy_():
  global CONFIG
  if not bstack111l1ll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭औ") in CONFIG[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")]:
    return
  bstack1ll111l1l_opy_ = datetime.datetime.now()
  bstack1lllllll1l_opy_ = bstack1ll111l1l_opy_.strftime(bstack111l1ll_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧख"))
  CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग")] = CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")].replace(
    bstack111l1ll_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫङ"),
    bstack1lllllll1l_opy_
  )
def bstack11l1l1111_opy_():
  global CONFIG
  if bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच") in CONFIG and not bool(CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")]):
    del CONFIG[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")]
    return
  if not bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG:
    CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = bstack111l1ll_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧट")
  if bstack111l1ll_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫठ") in CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")]:
    bstack1l1l111ll_opy_()
    os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫढ")] = CONFIG[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण")]
  if not bstack111l1ll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫत") in CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    return
  bstack11l1ll111_opy_ = bstack111l1ll_opy_ (u"ࠫࠬद")
  bstack1lll1llll_opy_ = bstack11llll1111_opy_()
  if bstack1lll1llll_opy_ != -1:
    bstack11l1ll111_opy_ = bstack111l1ll_opy_ (u"ࠬࡉࡉࠡࠩध") + str(bstack1lll1llll_opy_)
  if bstack11l1ll111_opy_ == bstack111l1ll_opy_ (u"࠭ࠧन"):
    bstack1llll11111_opy_ = bstack1l1ll111l_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪऩ")])
    if bstack1llll11111_opy_ != -1:
      bstack11l1ll111_opy_ = str(bstack1llll11111_opy_)
  if bstack11l1ll111_opy_:
    bstack1lll11llll_opy_(bstack11l1ll111_opy_)
    os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬप")] = CONFIG[bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
def bstack1ll1l1ll11_opy_(bstack11ll1l11l_opy_, bstack1l1ll1ll_opy_, path):
  bstack11ll11l111_opy_ = {
    bstack111l1ll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧब"): bstack1l1ll1ll_opy_
  }
  if os.path.exists(path):
    bstack111111l1_opy_ = json.load(open(path, bstack111l1ll_opy_ (u"ࠫࡷࡨࠧभ")))
  else:
    bstack111111l1_opy_ = {}
  bstack111111l1_opy_[bstack11ll1l11l_opy_] = bstack11ll11l111_opy_
  with open(path, bstack111l1ll_opy_ (u"ࠧࡽࠫࠣम")) as outfile:
    json.dump(bstack111111l1_opy_, outfile)
def bstack1l1ll111l_opy_(bstack11ll1l11l_opy_):
  bstack11ll1l11l_opy_ = str(bstack11ll1l11l_opy_)
  bstack1l11lll1_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"࠭ࡾࠨय")), bstack111l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧर"))
  try:
    if not os.path.exists(bstack1l11lll1_opy_):
      os.makedirs(bstack1l11lll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠨࢀࠪऱ")), bstack111l1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩल"), bstack111l1ll_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬळ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l1ll_opy_ (u"ࠫࡼ࠭ऴ")):
        pass
      with open(file_path, bstack111l1ll_opy_ (u"ࠧࡽࠫࠣव")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l1ll_opy_ (u"࠭ࡲࠨश")) as bstack1llll111ll_opy_:
      bstack1l11ll1l1l_opy_ = json.load(bstack1llll111ll_opy_)
    if bstack11ll1l11l_opy_ in bstack1l11ll1l1l_opy_:
      bstack111111lll_opy_ = bstack1l11ll1l1l_opy_[bstack11ll1l11l_opy_][bstack111l1ll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫष")]
      bstack1ll1l11l_opy_ = int(bstack111111lll_opy_) + 1
      bstack1ll1l1ll11_opy_(bstack11ll1l11l_opy_, bstack1ll1l11l_opy_, file_path)
      return bstack1ll1l11l_opy_
    else:
      bstack1ll1l1ll11_opy_(bstack11ll1l11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l1l1lll_opy_.format(str(e)))
    return -1
def bstack1l1l1l1ll_opy_(config):
  if not config[bstack111l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪस")] or not config[bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬह")]:
    return True
  else:
    return False
def bstack111lll111_opy_(config, index=0):
  global bstack11l11l1l_opy_
  bstack11ll11l11l_opy_ = {}
  caps = bstack1ll1l1l1l1_opy_ + bstack1lll111111_opy_
  if config.get(bstack111l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧऺ"), False):
    bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨऻ")] = True
    bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")] = config.get(bstack111l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪऽ"), {})
  if bstack11l11l1l_opy_:
    caps += bstack1lll11ll11_opy_
  for key in config:
    if key in caps + [bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪा")]:
      continue
    bstack11ll11l11l_opy_[key] = config[key]
  if bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫि") in config:
    for bstack1llll1l1l1_opy_ in config[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬी")][index]:
      if bstack1llll1l1l1_opy_ in caps:
        continue
      bstack11ll11l11l_opy_[bstack1llll1l1l1_opy_] = config[bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")][index][bstack1llll1l1l1_opy_]
  bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ू")] = socket.gethostname()
  if bstack111l1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ृ") in bstack11ll11l11l_opy_:
    del (bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧॄ")])
  return bstack11ll11l11l_opy_
def bstack1l111ll11l_opy_(config):
  global bstack11l11l1l_opy_
  bstack1llllll1l_opy_ = {}
  caps = bstack1lll111111_opy_
  if bstack11l11l1l_opy_:
    caps += bstack1lll11ll11_opy_
  for key in caps:
    if key in config:
      bstack1llllll1l_opy_[key] = config[key]
  return bstack1llllll1l_opy_
def bstack1ll1l11l1l_opy_(bstack11ll11l11l_opy_, bstack1llllll1l_opy_):
  bstack1lll11111_opy_ = {}
  for key in bstack11ll11l11l_opy_.keys():
    if key in bstack11lllll11l_opy_:
      bstack1lll11111_opy_[bstack11lllll11l_opy_[key]] = bstack11ll11l11l_opy_[key]
    else:
      bstack1lll11111_opy_[key] = bstack11ll11l11l_opy_[key]
  for key in bstack1llllll1l_opy_:
    if key in bstack11lllll11l_opy_:
      bstack1lll11111_opy_[bstack11lllll11l_opy_[key]] = bstack1llllll1l_opy_[key]
    else:
      bstack1lll11111_opy_[key] = bstack1llllll1l_opy_[key]
  return bstack1lll11111_opy_
def bstack1ll11l1l_opy_(config, index=0):
  global bstack11l11l1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11lll1ll1_opy_ = bstack111l11ll_opy_(bstack11ll111ll1_opy_, config, logger)
  bstack1llllll1l_opy_ = bstack1l111ll11l_opy_(config)
  bstack1l1l111l1_opy_ = bstack1lll111111_opy_
  bstack1l1l111l1_opy_ += bstack111111111_opy_
  bstack1llllll1l_opy_ = update(bstack1llllll1l_opy_, bstack11lll1ll1_opy_)
  if bstack11l11l1l_opy_:
    bstack1l1l111l1_opy_ += bstack1lll11ll11_opy_
  if bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ") in config:
    if bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॆ") in config[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")][index]:
      caps[bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨै")] = config[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index][bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ")]
    if bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧो") in config[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index]:
      caps[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯्ࠩ")] = str(config[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ")])
    bstack1l11111l1l_opy_ = bstack111l11ll_opy_(bstack11ll111ll1_opy_, config[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index], logger)
    bstack1l1l111l1_opy_ += list(bstack1l11111l1l_opy_.keys())
    for bstack1l1l1l11l1_opy_ in bstack1l1l111l1_opy_:
      if bstack1l1l1l11l1_opy_ in config[bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
        if bstack1l1l1l11l1_opy_ == bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॒"):
          try:
            bstack1l11111l1l_opy_[bstack1l1l1l11l1_opy_] = str(config[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1l1l1l11l1_opy_] * 1.0)
          except:
            bstack1l11111l1l_opy_[bstack1l1l1l11l1_opy_] = str(config[bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index][bstack1l1l1l11l1_opy_])
        else:
          bstack1l11111l1l_opy_[bstack1l1l1l11l1_opy_] = config[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index][bstack1l1l1l11l1_opy_]
        del (config[bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l1l1l11l1_opy_])
    bstack1llllll1l_opy_ = update(bstack1llllll1l_opy_, bstack1l11111l1l_opy_)
  bstack11ll11l11l_opy_ = bstack111lll111_opy_(config, index)
  for bstack1ll11llll_opy_ in bstack1lll111111_opy_ + list(bstack11lll1ll1_opy_.keys()):
    if bstack1ll11llll_opy_ in bstack11ll11l11l_opy_:
      bstack1llllll1l_opy_[bstack1ll11llll_opy_] = bstack11ll11l11l_opy_[bstack1ll11llll_opy_]
      del (bstack11ll11l11l_opy_[bstack1ll11llll_opy_])
  if bstack1l111lll1_opy_(config):
    bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫॗ")] = True
    caps.update(bstack1llllll1l_opy_)
    caps[bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭क़")] = bstack11ll11l11l_opy_
  else:
    bstack11ll11l11l_opy_[bstack111l1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ख़")] = False
    caps.update(bstack1ll1l11l1l_opy_(bstack11ll11l11l_opy_, bstack1llllll1l_opy_))
    if bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬग़") in caps:
      caps[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩज़")] = caps[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")]
      del (caps[bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")])
    if bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़") in caps:
      caps[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧय़")] = caps[bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॠ")]
      del (caps[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ")])
  return caps
def bstack1l1111l1l1_opy_():
  global bstack1lll11l111_opy_
  global CONFIG
  if bstack1llll11lll_opy_() <= version.parse(bstack111l1ll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨॢ")):
    if bstack1lll11l111_opy_ != bstack111l1ll_opy_ (u"ࠩࠪॣ"):
      return bstack111l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ।") + bstack1lll11l111_opy_ + bstack111l1ll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ॥")
    return bstack1lllllllll_opy_
  if bstack1lll11l111_opy_ != bstack111l1ll_opy_ (u"ࠬ࠭०"):
    return bstack111l1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ१") + bstack1lll11l111_opy_ + bstack111l1ll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ२")
  return bstack111111l1l_opy_
def bstack1lll11ll1l_opy_(options):
  return hasattr(options, bstack111l1ll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ३"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1l11ll1_opy_(options, bstack1l1ll1llll_opy_):
  for bstack1lllll1l1_opy_ in bstack1l1ll1llll_opy_:
    if bstack1lllll1l1_opy_ in [bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ४"), bstack111l1ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ५")]:
      continue
    if bstack1lllll1l1_opy_ in options._experimental_options:
      options._experimental_options[bstack1lllll1l1_opy_] = update(options._experimental_options[bstack1lllll1l1_opy_],
                                                         bstack1l1ll1llll_opy_[bstack1lllll1l1_opy_])
    else:
      options.add_experimental_option(bstack1lllll1l1_opy_, bstack1l1ll1llll_opy_[bstack1lllll1l1_opy_])
  if bstack111l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ६") in bstack1l1ll1llll_opy_:
    for arg in bstack1l1ll1llll_opy_[bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪ७")]:
      options.add_argument(arg)
    del (bstack1l1ll1llll_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ८")])
  if bstack111l1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९") in bstack1l1ll1llll_opy_:
    for ext in bstack1l1ll1llll_opy_[bstack111l1ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ॰")]:
      options.add_extension(ext)
    del (bstack1l1ll1llll_opy_[bstack111l1ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॱ")])
def bstack1l111111_opy_(options, bstack1lll1lll11_opy_):
  if bstack111l1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॲ") in bstack1lll1lll11_opy_:
    for bstack1llllll111_opy_ in bstack1lll1lll11_opy_[bstack111l1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪॳ")]:
      if bstack1llllll111_opy_ in options._preferences:
        options._preferences[bstack1llllll111_opy_] = update(options._preferences[bstack1llllll111_opy_], bstack1lll1lll11_opy_[bstack111l1ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॴ")][bstack1llllll111_opy_])
      else:
        options.set_preference(bstack1llllll111_opy_, bstack1lll1lll11_opy_[bstack111l1ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ")][bstack1llllll111_opy_])
  if bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack1lll1lll11_opy_:
    for arg in bstack1lll1lll11_opy_[bstack111l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
def bstack111l1llll_opy_(options, bstack111l111l1_opy_):
  if bstack111l1ll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪॸ") in bstack111l111l1_opy_:
    options.use_webview(bool(bstack111l111l1_opy_[bstack111l1ll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫॹ")]))
  bstack1ll1l11ll1_opy_(options, bstack111l111l1_opy_)
def bstack1ll1111l1_opy_(options, bstack1l11l1l11_opy_):
  for bstack1ll1l11lll_opy_ in bstack1l11l1l11_opy_:
    if bstack1ll1l11lll_opy_ in [bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨॺ"), bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      continue
    options.set_capability(bstack1ll1l11lll_opy_, bstack1l11l1l11_opy_[bstack1ll1l11lll_opy_])
  if bstack111l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1l11l1l11_opy_:
    for arg in bstack1l11l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
  if bstack111l1ll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ") in bstack1l11l1l11_opy_:
    options.bstack11111ll1l_opy_(bool(bstack1l11l1l11_opy_[bstack111l1ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ॿ")]))
def bstack1111l11ll_opy_(options, bstack11l11ll1l_opy_):
  for bstack1lllll11_opy_ in bstack11l11ll1l_opy_:
    if bstack1lllll11_opy_ in [bstack111l1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧঀ"), bstack111l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      continue
    options._options[bstack1lllll11_opy_] = bstack11l11ll1l_opy_[bstack1lllll11_opy_]
  if bstack111l1ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩং") in bstack11l11ll1l_opy_:
    for bstack1111llll_opy_ in bstack11l11ll1l_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ")]:
      options.bstack111l1ll1l_opy_(
        bstack1111llll_opy_, bstack11l11ll1l_opy_[bstack111l1ll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄")][bstack1111llll_opy_])
  if bstack111l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack11l11ll1l_opy_:
    for arg in bstack11l11ll1l_opy_[bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
def bstack1l1l1l1l11_opy_(options, caps):
  if not hasattr(options, bstack111l1ll_opy_ (u"ࠪࡏࡊ࡟ࠧই")):
    return
  if options.KEY == bstack111l1ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঈ") and options.KEY in caps:
    bstack1ll1l11ll1_opy_(options, caps[bstack111l1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪউ")])
  elif options.KEY == bstack111l1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঊ") and options.KEY in caps:
    bstack1l111111_opy_(options, caps[bstack111l1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঋ")])
  elif options.KEY == bstack111l1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঌ") and options.KEY in caps:
    bstack1ll1111l1_opy_(options, caps[bstack111l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঍")])
  elif options.KEY == bstack111l1ll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ঎") and options.KEY in caps:
    bstack111l1llll_opy_(options, caps[bstack111l1ll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬএ")])
  elif options.KEY == bstack111l1ll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঐ") and options.KEY in caps:
    bstack1111l11ll_opy_(options, caps[bstack111l1ll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঑")])
def bstack11ll1l111_opy_(caps):
  global bstack11l11l1l_opy_
  if isinstance(os.environ.get(bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ঒")), str):
    bstack11l11l1l_opy_ = eval(os.getenv(bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩও")))
  if bstack11l11l1l_opy_:
    if bstack111ll1lll_opy_() < version.parse(bstack111l1ll_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঔ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪক")
    if bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ") in caps:
      browser = caps[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ")]
    elif bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঘ") in caps:
      browser = caps[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨঙ")]
    browser = str(browser).lower()
    if browser == bstack111l1ll_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨচ") or browser == bstack111l1ll_opy_ (u"ࠩ࡬ࡴࡦࡪࠧছ"):
      browser = bstack111l1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪজ")
    if browser == bstack111l1ll_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬঝ"):
      browser = bstack111l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬঞ")
    if browser not in [bstack111l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট"), bstack111l1ll_opy_ (u"ࠧࡦࡦࡪࡩࠬঠ"), bstack111l1ll_opy_ (u"ࠨ࡫ࡨࠫড"), bstack111l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩঢ"), bstack111l1ll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫণ")]:
      return None
    try:
      package = bstack111l1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ত").format(browser)
      name = bstack111l1ll_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll11ll1l_opy_(options):
        return None
      for bstack1ll11llll_opy_ in caps.keys():
        options.set_capability(bstack1ll11llll_opy_, caps[bstack1ll11llll_opy_])
      bstack1l1l1l1l11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11111ll11_opy_(options, bstack1lll111ll_opy_):
  if not bstack1lll11ll1l_opy_(options):
    return
  for bstack1ll11llll_opy_ in bstack1lll111ll_opy_.keys():
    if bstack1ll11llll_opy_ in bstack111111111_opy_:
      continue
    if bstack1ll11llll_opy_ in options._caps and type(options._caps[bstack1ll11llll_opy_]) in [dict, list]:
      options._caps[bstack1ll11llll_opy_] = update(options._caps[bstack1ll11llll_opy_], bstack1lll111ll_opy_[bstack1ll11llll_opy_])
    else:
      options.set_capability(bstack1ll11llll_opy_, bstack1lll111ll_opy_[bstack1ll11llll_opy_])
  bstack1l1l1l1l11_opy_(options, bstack1lll111ll_opy_)
  if bstack111l1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬদ") in options._caps:
    if options._caps[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬধ")] and options._caps[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ন")].lower() != bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ঩"):
      del options._caps[bstack111l1ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ")]
def bstack111llll1_opy_(proxy_config):
  if bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in proxy_config:
    proxy_config[bstack111l1ll_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧব")] = proxy_config[bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
    del (proxy_config[bstack111l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")])
  if bstack111l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫয") in proxy_config and proxy_config[bstack111l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬর")].lower() != bstack111l1ll_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ঱"):
    proxy_config[bstack111l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল")] = bstack111l1ll_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬ঳")
  if bstack111l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ঴") in proxy_config:
    proxy_config[bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack111l1ll_opy_ (u"ࠨࡲࡤࡧࠬশ")
  return proxy_config
def bstack1ll1111l1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨষ") in config:
    return proxy
  config[bstack111l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩস")] = bstack111llll1_opy_(config[bstack111l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪহ")])
  if proxy == None:
    proxy = Proxy(config[bstack111l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺")])
  return proxy
def bstack1l11l111_opy_(self):
  global CONFIG
  global bstack1l1llllll_opy_
  try:
    proxy = bstack1ll1111111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l1ll_opy_ (u"࠭࠮ࡱࡣࡦࠫ঻")):
        proxies = bstack1111llll1_opy_(proxy, bstack1l1111l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1llll1_opy_ = proxies.popitem()
          if bstack111l1ll_opy_ (u"ࠢ࠻࠱࠲়ࠦ") in bstack1ll1llll1_opy_:
            return bstack1ll1llll1_opy_
          else:
            return bstack111l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤঽ") + bstack1ll1llll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨা").format(str(e)))
  return bstack1l1llllll_opy_(self)
def bstack1l1llll1ll_opy_():
  global CONFIG
  return bstack1lll1ll1l1_opy_(CONFIG) and bstack1l11ll1l_opy_() and bstack1llll11lll_opy_() >= version.parse(bstack11lllll1ll_opy_)
def bstack1llll1lll_opy_():
  global CONFIG
  return (bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ি") in CONFIG or bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in CONFIG) and bstack11ll1ll1ll_opy_()
def bstack1lll1l1l_opy_(config):
  bstack1l1lll11l1_opy_ = {}
  if bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩু") in config:
    bstack1l1lll11l1_opy_ = config[bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪূ")]
  if bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৃ") in config:
    bstack1l1lll11l1_opy_ = config[bstack111l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৄ")]
  proxy = bstack1ll1111111_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")) and os.path.isfile(proxy):
      bstack1l1lll11l1_opy_[bstack111l1ll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৆")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l1ll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩে")):
        proxies = bstack1111l1l1_opy_(config, bstack1l1111l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1llll1_opy_ = proxies.popitem()
          if bstack111l1ll_opy_ (u"ࠧࡀ࠯࠰ࠤৈ") in bstack1ll1llll1_opy_:
            parsed_url = urlparse(bstack1ll1llll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l1ll_opy_ (u"ࠨ࠺࠰࠱ࠥ৉") + bstack1ll1llll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1lll11l1_opy_[bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৊")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1lll11l1_opy_[bstack111l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫো")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1lll11l1_opy_[bstack111l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৌ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1lll11l1_opy_[bstack111l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ্࠭")] = str(parsed_url.password)
  return bstack1l1lll11l1_opy_
def bstack1ll1l1l1ll_opy_(config):
  if bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৎ") in config:
    return config[bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৏")]
  return {}
def bstack1l111l1111_opy_(caps):
  global bstack1l1ll1l11l_opy_
  if bstack111l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৐") in caps:
    caps[bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৑")][bstack111l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৒")] = True
    if bstack1l1ll1l11l_opy_:
      caps[bstack111l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓")][bstack111l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")] = bstack1l1ll1l11l_opy_
  else:
    caps[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৕")] = True
    if bstack1l1ll1l11l_opy_:
      caps[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৖")] = bstack1l1ll1l11l_opy_
@measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1llllll1ll_opy_():
  global CONFIG
  if not bstack1llllll11_opy_(CONFIG):
    return
  if bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪৗ") in CONFIG and bstack1l1111111_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৘")]):
    if (
      bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৙") in CONFIG
      and bstack1l1111111_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৚")].get(bstack111l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৛")))
    ):
      logger.debug(bstack111l1ll_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧড়"))
      return
    bstack1l1lll11l1_opy_ = bstack1lll1l1l_opy_(CONFIG)
    bstack11ll1ll111_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঢ়")], bstack1l1lll11l1_opy_)
def bstack11ll1ll111_opy_(key, bstack1l1lll11l1_opy_):
  global bstack1111l1111_opy_
  logger.info(bstack1lll1llll1_opy_)
  try:
    bstack1111l1111_opy_ = Local()
    bstack11ll1llll_opy_ = {bstack111l1ll_opy_ (u"࠭࡫ࡦࡻࠪ৞"): key}
    bstack11ll1llll_opy_.update(bstack1l1lll11l1_opy_)
    logger.debug(bstack1111l1lll_opy_.format(str(bstack11ll1llll_opy_)))
    bstack1111l1111_opy_.start(**bstack11ll1llll_opy_)
    if bstack1111l1111_opy_.isRunning():
      logger.info(bstack1l1l111111_opy_)
  except Exception as e:
    bstack1ll1l111ll_opy_(bstack1lllllll11_opy_.format(str(e)))
def bstack11l1ll1l_opy_():
  global bstack1111l1111_opy_
  if bstack1111l1111_opy_.isRunning():
    logger.info(bstack111l1l1l1_opy_)
    bstack1111l1111_opy_.stop()
  bstack1111l1111_opy_ = None
def bstack11ll1l11l1_opy_(bstack1l111l1l1_opy_=[]):
  global CONFIG
  bstack111l1l11l_opy_ = []
  bstack11ll1ll1l_opy_ = [bstack111l1ll_opy_ (u"ࠧࡰࡵࠪয়"), bstack111l1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫৠ"), bstack111l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ৡ"), bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৢ"), bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩৣ"), bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৤")]
  try:
    for err in bstack1l111l1l1_opy_:
      bstack1l1llll11_opy_ = {}
      for k in bstack11ll1ll1l_opy_:
        val = CONFIG[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][int(err[bstack111l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭০")])].get(k)
        if val:
          bstack1l1llll11_opy_[k] = val
      if(err[bstack111l1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ১")] != bstack111l1ll_opy_ (u"ࠩࠪ২")):
        bstack1l1llll11_opy_[bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ৩")] = {
          err[bstack111l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ৪")]: err[bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")]
        }
        bstack111l1l11l_opy_.append(bstack1l1llll11_opy_)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ৬") + str(e))
  finally:
    return bstack111l1l11l_opy_
def bstack11l1llllll_opy_(file_name):
  bstack1l1lll1ll1_opy_ = []
  try:
    bstack1lll1lll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lll1lll_opy_):
      with open(bstack1lll1lll_opy_) as f:
        bstack1l1ll111l1_opy_ = json.load(f)
        bstack1l1lll1ll1_opy_ = bstack1l1ll111l1_opy_
      os.remove(bstack1lll1lll_opy_)
    return bstack1l1lll1ll1_opy_
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ৭") + str(e))
    return bstack1l1lll1ll1_opy_
def bstack1l1l11l1ll_opy_():
  try:
      from bstack_utils.constants import bstack11lll1l11_opy_, EVENTS
      from bstack_utils.helper import bstack11ll1111_opy_, get_host_info, bstack1ll11lll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack11l1ll1l1_opy_ = os.path.join(os.getcwd(), bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ৮"), bstack111l1ll_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬ৯"))
      lock = FileLock(bstack11l1ll1l1_opy_+bstack111l1ll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤৰ"))
      def bstack1ll111lll_opy_():
          try:
              with lock:
                  with open(bstack11l1ll1l1_opy_, bstack111l1ll_opy_ (u"ࠦࡷࠨৱ"), encoding=bstack111l1ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ৲")) as file:
                      data = json.load(file)
                      config = {
                          bstack111l1ll_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ৳"): {
                              bstack111l1ll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨ৴"): bstack111l1ll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦ৵"),
                          }
                      }
                      bstack1l1ll11l_opy_ = datetime.utcnow()
                      bstack1ll111l1l_opy_ = bstack1l1ll11l_opy_.strftime(bstack111l1ll_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠢࡘࡘࡈࠨ৶"))
                      bstack1l1ll1ll11_opy_ = os.environ.get(bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ৷")) if os.environ.get(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ৸")) else bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ৹"))
                      payload = {
                          bstack111l1ll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠥ৺"): bstack111l1ll_opy_ (u"ࠢࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦ৻"),
                          bstack111l1ll_opy_ (u"ࠣࡦࡤࡸࡦࠨৼ"): {
                              bstack111l1ll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠣ৽"): bstack1l1ll1ll11_opy_,
                              bstack111l1ll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࡣࡩࡧࡹࠣ৾"): bstack1ll111l1l_opy_,
                              bstack111l1ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࠣ৿"): bstack111l1ll_opy_ (u"࡙ࠧࡄࡌࡈࡨࡥࡹࡻࡲࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࠨ਀"),
                              bstack111l1ll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡰࡳࡰࡰࠥਁ"): {
                                  bstack111l1ll_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࡴࠤਂ"): data,
                                  bstack111l1ll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥਃ"): bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ਄"))
                              },
                              bstack111l1ll_opy_ (u"ࠥࡹࡸ࡫ࡲࡠࡦࡤࡸࡦࠨਅ"): bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨਆ")),
                              bstack111l1ll_opy_ (u"ࠧ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠣਇ"): get_host_info()
                          }
                      }
                      response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠨࡐࡐࡕࡗࠦਈ"), bstack11lll1l11_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack111l1ll_opy_ (u"ࠢࡅࡣࡷࡥࠥࡹࡥ࡯ࡶࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡷࡳࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦࡤࡢࡶࡤࠤࢀࢃࠢਉ").format(bstack11lll1l11_opy_, payload))
                      else:
                          logger.debug(bstack111l1ll_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡩࡳࡷࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࠥࢁࡽࠣਊ").format(bstack11lll1l11_opy_, payload))
          except Exception as e:
              logger.debug(bstack111l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣࡿࢂࠨ਋").format(e))
      bstack1ll111lll_opy_()
      bstack1l11ll11_opy_(bstack11l1ll1l1_opy_, logger)
  except:
    pass
def bstack1111ll1ll_opy_():
  global bstack11111lll1_opy_
  global bstack1ll1ll11ll_opy_
  global bstack11lll11l_opy_
  global bstack1ll1llll_opy_
  global bstack1l1l111l1l_opy_
  global bstack1l1ll1111l_opy_
  global CONFIG
  bstack11lll1lll_opy_ = os.environ.get(bstack111l1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ਌"))
  if bstack11lll1lll_opy_ in [bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ਍"), bstack111l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ਎")]:
    bstack11111lll_opy_()
  percy.shutdown()
  if bstack11111lll1_opy_:
    logger.warning(bstack1ll1l1ll1_opy_.format(str(bstack11111lll1_opy_)))
  else:
    try:
      bstack111111l1_opy_ = bstack1l111ll11_opy_(bstack111l1ll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬਏ"), logger)
      if bstack111111l1_opy_.get(bstack111l1ll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਐ")) and bstack111111l1_opy_.get(bstack111l1ll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭਑")).get(bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ਒")):
        logger.warning(bstack1ll1l1ll1_opy_.format(str(bstack111111l1_opy_[bstack111l1ll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨਓ")][bstack111l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ਔ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l1lll1111_opy_)
  global bstack1111l1111_opy_
  if bstack1111l1111_opy_:
    bstack11l1ll1l_opy_()
  try:
    for driver in bstack1ll1ll11ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1ll1l1ll_opy_)
  if bstack1l1ll1111l_opy_ == bstack111l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ"):
    bstack1l1l111l1l_opy_ = bstack11l1llllll_opy_(bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧਖ"))
  if bstack1l1ll1111l_opy_ == bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਗ") and len(bstack1ll1llll_opy_) == 0:
    bstack1ll1llll_opy_ = bstack11l1llllll_opy_(bstack111l1ll_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਘ"))
    if len(bstack1ll1llll_opy_) == 0:
      bstack1ll1llll_opy_ = bstack11l1llllll_opy_(bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨਙ"))
  bstack111llllll_opy_ = bstack111l1ll_opy_ (u"ࠪࠫਚ")
  if len(bstack11lll11l_opy_) > 0:
    bstack111llllll_opy_ = bstack11ll1l11l1_opy_(bstack11lll11l_opy_)
  elif len(bstack1ll1llll_opy_) > 0:
    bstack111llllll_opy_ = bstack11ll1l11l1_opy_(bstack1ll1llll_opy_)
  elif len(bstack1l1l111l1l_opy_) > 0:
    bstack111llllll_opy_ = bstack11ll1l11l1_opy_(bstack1l1l111l1l_opy_)
  elif len(bstack1ll1llllll_opy_) > 0:
    bstack111llllll_opy_ = bstack11ll1l11l1_opy_(bstack1ll1llllll_opy_)
  if bool(bstack111llllll_opy_):
    bstack1111l1ll1_opy_(bstack111llllll_opy_)
  else:
    bstack1111l1ll1_opy_()
  bstack1l11ll11_opy_(bstack11l1llll_opy_, logger)
  if bstack11lll1lll_opy_ not in [bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬਛ")]:
    bstack1l1l11l1ll_opy_()
  bstack1111ll11_opy_.bstack11lll111l_opy_(CONFIG)
  if len(bstack1l1l111l1l_opy_) > 0:
    sys.exit(len(bstack1l1l111l1l_opy_))
def bstack111ll111_opy_(bstack1l1lll11l_opy_, frame):
  global bstack1ll11lll_opy_
  logger.error(bstack1111lllll_opy_)
  bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨਜ"), bstack1l1lll11l_opy_)
  if hasattr(signal, bstack111l1ll_opy_ (u"࠭ࡓࡪࡩࡱࡥࡱࡹࠧਝ")):
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧਞ"), signal.Signals(bstack1l1lll11l_opy_).name)
  else:
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨਟ"), bstack111l1ll_opy_ (u"ࠩࡖࡍࡌ࡛ࡎࡌࡐࡒ࡛ࡓ࠭ਠ"))
  bstack11lll1lll_opy_ = os.environ.get(bstack111l1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫਡ"))
  if bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਢ"):
    bstack1lll1ll111_opy_.stop(bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ")))
  bstack1111ll1ll_opy_()
  sys.exit(1)
def bstack1ll1l111ll_opy_(err):
  logger.critical(bstack1l111l111l_opy_.format(str(err)))
  bstack1111l1ll1_opy_(bstack1l111l111l_opy_.format(str(err)), True)
  atexit.unregister(bstack1111ll1ll_opy_)
  bstack11111lll_opy_()
  sys.exit(1)
def bstack1lll11ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1111l1ll1_opy_(message, True)
  atexit.unregister(bstack1111ll1ll_opy_)
  bstack11111lll_opy_()
  sys.exit(1)
def bstack1ll11l11ll_opy_():
  global CONFIG
  global bstack1l11l11l1l_opy_
  global bstack1ll1lll1_opy_
  global bstack1ll1ll11l_opy_
  CONFIG = bstack1lllll111l_opy_()
  load_dotenv(CONFIG.get(bstack111l1ll_opy_ (u"࠭ࡥ࡯ࡸࡉ࡭ࡱ࡫ࠧਤ")))
  bstack11llll1l11_opy_()
  bstack1l11lll11l_opy_()
  CONFIG = bstack1ll11ll1l_opy_(CONFIG)
  update(CONFIG, bstack1ll1lll1_opy_)
  update(CONFIG, bstack1l11l11l1l_opy_)
  CONFIG = bstack1l1111l1_opy_(CONFIG)
  bstack1ll1ll11l_opy_ = bstack1llllll11_opy_(CONFIG)
  os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪਥ")] = bstack1ll1ll11l_opy_.__str__()
  bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩਦ"), bstack1ll1ll11l_opy_)
  if (bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਧ") in CONFIG and bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਨ") in bstack1l11l11l1l_opy_) or (
          bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਩") in CONFIG and bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨਪ") not in bstack1ll1lll1_opy_):
    if os.getenv(bstack111l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਫ")):
      CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਬ")] = os.getenv(bstack111l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬਭ"))
    else:
      bstack11l1l1111_opy_()
  elif (bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in CONFIG and bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਯ") in CONFIG) or (
          bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਰ") in bstack1ll1lll1_opy_ and bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ਱") not in bstack1l11l11l1l_opy_):
    del (CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਲ")])
  if bstack1l1l1l1ll_opy_(CONFIG):
    bstack1ll1l111ll_opy_(bstack1l11ll1lll_opy_)
  Config.bstack1l1ll1l1_opy_().bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤਲ਼"), CONFIG[bstack111l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ਴")])
  bstack1l1lllllll_opy_()
  bstack11lllllll1_opy_()
  if bstack11l11l1l_opy_:
    CONFIG[bstack111l1ll_opy_ (u"ࠩࡤࡴࡵ࠭ਵ")] = bstack11ll11ll1_opy_(CONFIG)
    logger.info(bstack1ll1111ll_opy_.format(CONFIG[bstack111l1ll_opy_ (u"ࠪࡥࡵࡶࠧਸ਼")]))
  if not bstack1ll1ll11l_opy_:
    CONFIG[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਷")] = [{}]
def bstack1ll1lll111_opy_(config, bstack1111l1l11_opy_):
  global CONFIG
  global bstack11l11l1l_opy_
  CONFIG = config
  bstack11l11l1l_opy_ = bstack1111l1l11_opy_
def bstack11lllllll1_opy_():
  global CONFIG
  global bstack11l11l1l_opy_
  if bstack111l1ll_opy_ (u"ࠬࡧࡰࡱࠩਸ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1llll11ll1_opy_)
    bstack11l11l1l_opy_ = True
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬਹ"), True)
def bstack11ll11ll1_opy_(config):
  bstack11ll111ll_opy_ = bstack111l1ll_opy_ (u"ࠧࠨ਺")
  app = config[bstack111l1ll_opy_ (u"ࠨࡣࡳࡴࠬ਻")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1l1lll_opy_:
      if os.path.exists(app):
        bstack11ll111ll_opy_ = bstack1l11l1ll11_opy_(config, app)
      elif bstack111l1111l_opy_(app):
        bstack11ll111ll_opy_ = app
      else:
        bstack1ll1l111ll_opy_(bstack1ll1ll11_opy_.format(app))
    else:
      if bstack111l1111l_opy_(app):
        bstack11ll111ll_opy_ = app
      elif os.path.exists(app):
        bstack11ll111ll_opy_ = bstack1l11l1ll11_opy_(app)
      else:
        bstack1ll1l111ll_opy_(bstack11ll11l1_opy_)
  else:
    if len(app) > 2:
      bstack1ll1l111ll_opy_(bstack1l11l1l1ll_opy_)
    elif len(app) == 2:
      if bstack111l1ll_opy_ (u"ࠩࡳࡥࡹ࡮਼ࠧ") in app and bstack111l1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭਽") in app:
        if os.path.exists(app[bstack111l1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩਾ")]):
          bstack11ll111ll_opy_ = bstack1l11l1ll11_opy_(config, app[bstack111l1ll_opy_ (u"ࠬࡶࡡࡵࡪࠪਿ")], app[bstack111l1ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩੀ")])
        else:
          bstack1ll1l111ll_opy_(bstack1ll1ll11_opy_.format(app))
      else:
        bstack1ll1l111ll_opy_(bstack1l11l1l1ll_opy_)
    else:
      for key in app:
        if key in bstack111111ll1_opy_:
          if key == bstack111l1ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬੁ"):
            if os.path.exists(app[key]):
              bstack11ll111ll_opy_ = bstack1l11l1ll11_opy_(config, app[key])
            else:
              bstack1ll1l111ll_opy_(bstack1ll1ll11_opy_.format(app))
          else:
            bstack11ll111ll_opy_ = app[key]
        else:
          bstack1ll1l111ll_opy_(bstack1l1l1111_opy_)
  return bstack11ll111ll_opy_
def bstack111l1111l_opy_(bstack11ll111ll_opy_):
  import re
  bstack1l11llll_opy_ = re.compile(bstack111l1ll_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣੂ"))
  bstack1lll11l1ll_opy_ = re.compile(bstack111l1ll_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪ࠰࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ੃"))
  if bstack111l1ll_opy_ (u"ࠪࡦࡸࡀ࠯࠰ࠩ੄") in bstack11ll111ll_opy_ or re.fullmatch(bstack1l11llll_opy_, bstack11ll111ll_opy_) or re.fullmatch(bstack1lll11l1ll_opy_, bstack11ll111ll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1l1l111l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1l11l1ll11_opy_(config, path, bstack1lllll1ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l1ll_opy_ (u"ࠫࡷࡨࠧ੅")).read()).hexdigest()
  bstack1lll1111ll_opy_ = bstack11lll1ll1l_opy_(md5_hash)
  bstack11ll111ll_opy_ = None
  if bstack1lll1111ll_opy_:
    logger.info(bstack1111111l1_opy_.format(bstack1lll1111ll_opy_, md5_hash))
    return bstack1lll1111ll_opy_
  bstack1lll1l1l11_opy_ = MultipartEncoder(
    fields={
      bstack111l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࠪ੆"): (os.path.basename(path), open(os.path.abspath(path), bstack111l1ll_opy_ (u"࠭ࡲࡣࠩੇ")), bstack111l1ll_opy_ (u"ࠧࡵࡧࡻࡸ࠴ࡶ࡬ࡢ࡫ࡱࠫੈ")),
      bstack111l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ੉"): bstack1lllll1ll1_opy_
    }
  )
  response = requests.post(bstack1ll111lll1_opy_, data=bstack1lll1l1l11_opy_,
                           headers={bstack111l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ੊"): bstack1lll1l1l11_opy_.content_type},
                           auth=(config[bstack111l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬੋ")], config[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧੌ")]))
  try:
    res = json.loads(response.text)
    bstack11ll111ll_opy_ = res[bstack111l1ll_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ੍࠭")]
    logger.info(bstack1ll1111ll1_opy_.format(bstack11ll111ll_opy_))
    bstack1l11ll11l1_opy_(md5_hash, bstack11ll111ll_opy_)
  except ValueError as err:
    bstack1ll1l111ll_opy_(bstack1lllll1l11_opy_.format(str(err)))
  return bstack11ll111ll_opy_
def bstack1l1lllllll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll11lll1l_opy_
  bstack11lllllll_opy_ = 1
  bstack1l11ll111_opy_ = 1
  if bstack111l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭੎") in CONFIG:
    bstack1l11ll111_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੏")]
  else:
    bstack1l11ll111_opy_ = bstack11ll1lll_opy_(framework_name, args) or 1
  if bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੐") in CONFIG:
    bstack11lllllll_opy_ = len(CONFIG[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬੑ")])
  bstack1ll11lll1l_opy_ = int(bstack1l11ll111_opy_) * int(bstack11lllllll_opy_)
def bstack11ll1lll_opy_(framework_name, args):
  if framework_name == bstack1ll111l1_opy_ and args and bstack111l1ll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ੒") in args:
      bstack1lllll1ll_opy_ = args.index(bstack111l1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ੓"))
      return int(args[bstack1lllll1ll_opy_ + 1]) or 1
  return 1
def bstack11lll1ll1l_opy_(md5_hash):
  bstack1111111ll_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠬࢄࠧ੔")), bstack111l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੕"), bstack111l1ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ੖"))
  if os.path.exists(bstack1111111ll_opy_):
    bstack11llll111_opy_ = json.load(open(bstack1111111ll_opy_, bstack111l1ll_opy_ (u"ࠨࡴࡥࠫ੗")))
    if md5_hash in bstack11llll111_opy_:
      bstack11l11111_opy_ = bstack11llll111_opy_[md5_hash]
      bstack11111l1l_opy_ = datetime.datetime.now()
      bstack1l1ll1l1l_opy_ = datetime.datetime.strptime(bstack11l11111_opy_[bstack111l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ੘")], bstack111l1ll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧਖ਼"))
      if (bstack11111l1l_opy_ - bstack1l1ll1l1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l11111_opy_[bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩਗ਼")]):
        return None
      return bstack11l11111_opy_[bstack111l1ll_opy_ (u"ࠬ࡯ࡤࠨਜ਼")]
  else:
    return None
def bstack1l11ll11l1_opy_(md5_hash, bstack11ll111ll_opy_):
  bstack1l11lll1_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"࠭ࡾࠨੜ")), bstack111l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੝"))
  if not os.path.exists(bstack1l11lll1_opy_):
    os.makedirs(bstack1l11lll1_opy_)
  bstack1111111ll_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠨࢀࠪਫ਼")), bstack111l1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੟"), bstack111l1ll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੠"))
  bstack1111l1ll_opy_ = {
    bstack111l1ll_opy_ (u"ࠫ࡮ࡪࠧ੡"): bstack11ll111ll_opy_,
    bstack111l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ੢"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l1ll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ੣")),
    bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ੤"): str(__version__)
  }
  if os.path.exists(bstack1111111ll_opy_):
    bstack11llll111_opy_ = json.load(open(bstack1111111ll_opy_, bstack111l1ll_opy_ (u"ࠨࡴࡥࠫ੥")))
  else:
    bstack11llll111_opy_ = {}
  bstack11llll111_opy_[md5_hash] = bstack1111l1ll_opy_
  with open(bstack1111111ll_opy_, bstack111l1ll_opy_ (u"ࠤࡺ࠯ࠧ੦")) as outfile:
    json.dump(bstack11llll111_opy_, outfile)
def bstack111lll1l_opy_(self):
  return
def bstack1l1l11llll_opy_(self):
  return
def bstack1l111lll_opy_(self):
  global bstack1l11111111_opy_
  bstack1l11111111_opy_(self)
def bstack1lll11l11_opy_():
  global bstack11lll1ll_opy_
  bstack11lll1ll_opy_ = True
@measure(event_name=EVENTS.bstack1l11l1ll1l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1llll11l1l_opy_(self):
  global bstack11ll1l1lll_opy_
  global bstack11ll1111l1_opy_
  global bstack1lllll11ll_opy_
  try:
    if bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ੧") in bstack11ll1l1lll_opy_ and self.session_id != None and bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ੨"), bstack111l1ll_opy_ (u"ࠬ࠭੩")) != bstack111l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ੪"):
      bstack1ll1ll1l11_opy_ = bstack111l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ੫") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ੬")
      if bstack1ll1ll1l11_opy_ == bstack111l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੭"):
        bstack1l1ll111_opy_(logger)
      if self != None:
        bstack11l1lllll1_opy_(self, bstack1ll1ll1l11_opy_, bstack111l1ll_opy_ (u"ࠪ࠰ࠥ࠭੮").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l1ll_opy_ (u"ࠫࠬ੯")
    if bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack11ll1l1lll_opy_ and getattr(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬੱ"), None):
      bstack1l1l11ll1l_opy_.bstack1l111l1ll1_opy_(self, bstack11ll1ll11l_opy_, logger, wait=True)
    if bstack111l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧੲ") in bstack11ll1l1lll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11l1lllll1_opy_(self, bstack111l1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣੳ"))
      bstack11ll1111ll_opy_.bstack11l1l1l1l_opy_(self)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥੴ") + str(e))
  bstack1lllll11ll_opy_(self)
  self.session_id = None
def bstack111ll1ll1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11l111ll_opy_
    global bstack11ll1l1lll_opy_
    command_executor = kwargs.get(bstack111l1ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ੵ"), bstack111l1ll_opy_ (u"ࠫࠬ੶"))
    bstack1llll111l_opy_ = False
    if type(command_executor) == str and bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ੷") in command_executor:
      bstack1llll111l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ੸") in str(getattr(command_executor, bstack111l1ll_opy_ (u"ࠧࡠࡷࡵࡰࠬ੹"), bstack111l1ll_opy_ (u"ࠨࠩ੺"))):
      bstack1llll111l_opy_ = True
    else:
      return bstack1ll111ll_opy_(self, *args, **kwargs)
    if bstack1llll111l_opy_:
      bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(CONFIG, bstack11ll1l1lll_opy_)
      if kwargs.get(bstack111l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ੻")):
        kwargs[bstack111l1ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ੼")] = bstack11l111ll_opy_(kwargs[bstack111l1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ੽")], bstack11ll1l1lll_opy_, bstack1l11ll1ll_opy_)
      elif kwargs.get(bstack111l1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ੾")):
        kwargs[bstack111l1ll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭੿")] = bstack11l111ll_opy_(kwargs[bstack111l1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ઀")], bstack11ll1l1lll_opy_, bstack1l11ll1ll_opy_)
  except Exception as e:
    logger.error(bstack111l1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣઁ").format(str(e)))
  return bstack1ll111ll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll1l1ll_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack111l1l1l_opy_(self, command_executor=bstack111l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱࠴࠶࠼࠴࠰࠯࠲࠱࠵࠿࠺࠴࠵࠶ࠥં"), *args, **kwargs):
  bstack11ll11l1l_opy_ = bstack111ll1ll1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l111ll1_opy_.on():
    return bstack11ll11l1l_opy_
  try:
    logger.debug(bstack111l1ll_opy_ (u"ࠪࡇࡴࡳ࡭ࡢࡰࡧࠤࡊࡾࡥࡤࡷࡷࡳࡷࠦࡷࡩࡧࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡪࡦࡲࡳࡦࠢ࠰ࠤࢀࢃࠧઃ").format(str(command_executor)))
    logger.debug(bstack111l1ll_opy_ (u"ࠫࡍࡻࡢࠡࡗࡕࡐࠥ࡯ࡳࠡ࠯ࠣࡿࢂ࠭઄").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઅ") in command_executor._url:
      bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧઆ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪઇ") in command_executor):
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩઈ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11llll1lll_opy_ = getattr(threading.current_thread(), bstack111l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪઉ"), None)
  if bstack111l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪઊ") in bstack11ll1l1lll_opy_ or bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪઋ") in bstack11ll1l1lll_opy_:
    bstack1lll1ll111_opy_.bstack1lllll1lll_opy_(self)
  if bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬઌ") in bstack11ll1l1lll_opy_ and bstack11llll1lll_opy_ and bstack11llll1lll_opy_.get(bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ઍ"), bstack111l1ll_opy_ (u"ࠧࠨ઎")) == bstack111l1ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩએ"):
    bstack1lll1ll111_opy_.bstack1lllll1lll_opy_(self)
  return bstack11ll11l1l_opy_
def bstack1111ll1l1_opy_(args):
  return bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪઐ") in str(args)
def bstack1ll11ll111_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l1ll_opy_
  global bstack1ll11l11l1_opy_
  bstack1l11l1llll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None)
  bstack11lll11l1l_opy_ = getattr(self, bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬઓ"), None) != None and getattr(self, bstack111l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ઔ"), None) == True
  if not bstack1ll11l11l1_opy_ and bstack1ll1ll11l_opy_ and bstack111l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧક") in CONFIG and CONFIG[bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨખ")] == True and bstack1l1111l111_opy_.bstack1ll1l11l11_opy_(driver_command) and (bstack11lll11l1l_opy_ or bstack1l11l1llll_opy_) and not bstack1111ll1l1_opy_(args):
    try:
      bstack1ll11l11l1_opy_ = True
      logger.debug(bstack111l1ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫગ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨઘ").format(str(err)))
    bstack1ll11l11l1_opy_ = False
  response = bstack1ll1l1ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪઙ") in str(bstack11ll1l1lll_opy_).lower() or bstack111l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬચ") in str(bstack11ll1l1lll_opy_).lower()) and bstack11l111ll1_opy_.on():
    try:
      if driver_command == bstack111l1ll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪછ"):
        bstack1lll1ll111_opy_.bstack1111lll1l_opy_({
            bstack111l1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭જ"): response[bstack111l1ll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧઝ")],
            bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩઞ"): bstack1lll1ll111_opy_.current_test_uuid() if bstack1lll1ll111_opy_.current_test_uuid() else bstack11l111ll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1l1lll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11ll1111l1_opy_
  global bstack1ll11l11l_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack111lll1ll_opy_
  global bstack1ll11l1l11_opy_
  global bstack11ll1l1lll_opy_
  global bstack1ll111ll_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1lll1111l_opy_
  global bstack11ll1ll11l_opy_
  CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬટ")] = str(bstack11ll1l1lll_opy_) + str(__version__)
  bstack1l111l11_opy_ = os.environ[bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩઠ")]
  bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(CONFIG, bstack11ll1l1lll_opy_)
  CONFIG[bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨડ")] = bstack1l111l11_opy_
  CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨઢ")] = bstack1l11ll1ll_opy_
  command_executor = bstack1l1111l1l1_opy_()
  logger.debug(bstack1l11lll111_opy_.format(command_executor))
  proxy = bstack1ll1111l1l_opy_(CONFIG, proxy)
  bstack11l111lll_opy_ = 0 if bstack1ll11l11l_opy_ < 0 else bstack1ll11l11l_opy_
  try:
    if bstack111lll1ll_opy_ is True:
      bstack11l111lll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11l1l11_opy_ is True:
      bstack11l111lll_opy_ = int(threading.current_thread().name)
  except:
    bstack11l111lll_opy_ = 0
  bstack1lll111ll_opy_ = bstack1ll11l1l_opy_(CONFIG, bstack11l111lll_opy_)
  logger.debug(bstack1llll11l_opy_.format(str(bstack1lll111ll_opy_)))
  if bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫણ") in CONFIG and bstack1l1111111_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬત")]):
    bstack1l111l1111_opy_(bstack1lll111ll_opy_)
  if bstack1l1llll111_opy_.bstack11llll1ll1_opy_(CONFIG, bstack11l111lll_opy_) and bstack1l1llll111_opy_.bstack11ll1l1l1_opy_(bstack1lll111ll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1l1llll111_opy_.set_capabilities(bstack1lll111ll_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll1l11_opy_ = bstack1ll11ll1l_opy_(desired_capabilities)
    bstack1lll1l11_opy_[bstack111l1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩથ")] = bstack1l111lll1_opy_(CONFIG)
    bstack1ll1ll1ll1_opy_ = bstack1ll11l1l_opy_(bstack1lll1l11_opy_)
    if bstack1ll1ll1ll1_opy_:
      bstack1lll111ll_opy_ = update(bstack1ll1ll1ll1_opy_, bstack1lll111ll_opy_)
    desired_capabilities = None
  if options:
    bstack11111ll11_opy_(options, bstack1lll111ll_opy_)
  if not options:
    options = bstack11ll1l111_opy_(bstack1lll111ll_opy_)
  bstack11ll1ll11l_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ"))[bstack11l111lll_opy_]
  if proxy and bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫધ")):
    options.proxy(proxy)
  if options and bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫન")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llll11lll_opy_() < version.parse(bstack111l1ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ઩")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll111ll_opy_)
  logger.info(bstack1lll1111l1_opy_)
  bstack1l1111ll1_opy_.end(EVENTS.bstack111lllll1_opy_.value, EVENTS.bstack111lllll1_opy_.value + bstack111l1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢપ"), EVENTS.bstack111lllll1_opy_.value + bstack111l1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨફ"), status=True, failure=None, test_name=bstack1ll1l1ll1l_opy_)
  if bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩબ")):
    bstack1ll111ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩભ")):
    bstack1ll111ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫમ")):
    bstack1ll111ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1ll111ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1111_opy_ = bstack111l1ll_opy_ (u"ࠬ࠭ય")
    if bstack1llll11lll_opy_() >= version.parse(bstack111l1ll_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧર")):
      bstack1lll1111_opy_ = self.caps.get(bstack111l1ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ઱"))
    else:
      bstack1lll1111_opy_ = self.capabilities.get(bstack111l1ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣલ"))
    if bstack1lll1111_opy_:
      bstack1ll1l1lll_opy_(bstack1lll1111_opy_)
      if bstack1llll11lll_opy_() <= version.parse(bstack111l1ll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩળ")):
        self.command_executor._url = bstack111l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ઴") + bstack1lll11l111_opy_ + bstack111l1ll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣવ")
      else:
        self.command_executor._url = bstack111l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢશ") + bstack1lll1111_opy_ + bstack111l1ll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢષ")
      logger.debug(bstack11l1llll1_opy_.format(bstack1lll1111_opy_))
    else:
      logger.debug(bstack1l11llll1l_opy_.format(bstack111l1ll_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣસ")))
  except Exception as e:
    logger.debug(bstack1l11llll1l_opy_.format(e))
  if bstack111l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧહ") in bstack11ll1l1lll_opy_:
    bstack111ll11l_opy_(bstack1ll11l11l_opy_, bstack1lll1111l_opy_)
  bstack11ll1111l1_opy_ = self.session_id
  if bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ઺") in bstack11ll1l1lll_opy_ or bstack111l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ઻") in bstack11ll1l1lll_opy_ or bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ઼ࠪ") in bstack11ll1l1lll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11llll1lll_opy_ = getattr(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ઽ"), None)
  if bstack111l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ા") in bstack11ll1l1lll_opy_ or bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭િ") in bstack11ll1l1lll_opy_:
    bstack1lll1ll111_opy_.bstack1lllll1lll_opy_(self)
  if bstack111l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨી") in bstack11ll1l1lll_opy_ and bstack11llll1lll_opy_ and bstack11llll1lll_opy_.get(bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩુ"), bstack111l1ll_opy_ (u"ࠪࠫૂ")) == bstack111l1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬૃ"):
    bstack1lll1ll111_opy_.bstack1lllll1lll_opy_(self)
  bstack1ll1ll11ll_opy_.append(self)
  if bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ") in CONFIG and bstack111l1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫૅ") in CONFIG[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૆")][bstack11l111lll_opy_]:
    bstack1ll1l1ll1l_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫે")][bstack11l111lll_opy_][bstack111l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧૈ")]
  logger.debug(bstack11llllllll_opy_.format(bstack11ll1111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1111llll_opy_
    def bstack11ll1l1111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l111l1l11_opy_
      if(bstack111l1ll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧૉ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠫࢃ࠭૊")), bstack111l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬો"), bstack111l1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨૌ")), bstack111l1ll_opy_ (u"ࠧࡸ્ࠩ")) as fp:
          fp.write(bstack111l1ll_opy_ (u"ࠣࠤ૎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l1ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ૏")))):
          with open(args[1], bstack111l1ll_opy_ (u"ࠪࡶࠬૐ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l1ll_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪ૑") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1ll11ll1_opy_)
            if bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ૒") in CONFIG and str(CONFIG[bstack111l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ૓")]).lower() != bstack111l1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭૔"):
                bstack111l111l_opy_ = bstack1l1111llll_opy_()
                bstack11l1ll11_opy_ = bstack111l1ll_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎࠥࠦࡴࡳࡻࠣࡿࢀࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࢀࠐࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࠩࡾࡧࡩࡶࡕࡳ࡮ࢀࠫࠥ࠱ࠠࡦࡰࡦࡳࡩ࡫ࡕࡓࡋࡆࡳࡲࡶ࡯࡯ࡧࡱࡸ࠭ࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡣࡢࡲࡶ࠭࠮࠲ࠊࠡࠢࠣࠤ࠳࠴࠮࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠊࠡࠢࢀࢁ࠮ࡁࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎࢂࢃ࠻ࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࠨࠩࠪ૕").format(bstack111l111l_opy_=bstack111l111l_opy_)
            lines.insert(1, bstack11l1ll11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l1ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ૖")), bstack111l1ll_opy_ (u"ࠪࡻࠬ૗")) as bstack1l1111l11_opy_:
              bstack1l1111l11_opy_.writelines(lines)
        CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭૘")] = str(bstack11ll1l1lll_opy_) + str(__version__)
        bstack1l111l11_opy_ = os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ૙")]
        bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(CONFIG, bstack11ll1l1lll_opy_)
        CONFIG[bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ૚")] = bstack1l111l11_opy_
        CONFIG[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ૛")] = bstack1l11ll1ll_opy_
        bstack11l111lll_opy_ = 0 if bstack1ll11l11l_opy_ < 0 else bstack1ll11l11l_opy_
        try:
          if bstack111lll1ll_opy_ is True:
            bstack11l111lll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11l1l11_opy_ is True:
            bstack11l111lll_opy_ = int(threading.current_thread().name)
        except:
          bstack11l111lll_opy_ = 0
        CONFIG[bstack111l1ll_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ૜")] = False
        CONFIG[bstack111l1ll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ૝")] = True
        bstack1lll111ll_opy_ = bstack1ll11l1l_opy_(CONFIG, bstack11l111lll_opy_)
        logger.debug(bstack1llll11l_opy_.format(str(bstack1lll111ll_opy_)))
        if CONFIG.get(bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૞")):
          bstack1l111l1111_opy_(bstack1lll111ll_opy_)
        if bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૟") in CONFIG and bstack111l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪૠ") in CONFIG[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")][bstack11l111lll_opy_]:
          bstack1ll1l1ll1l_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪૢ")][bstack11l111lll_opy_][bstack111l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ૣ")]
        args.append(os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠩࢁࠫ૤")), bstack111l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ૥"), bstack111l1ll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭૦")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll111ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l1ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ૧"))
      bstack1l111l1l11_opy_ = True
      return bstack1l1l1lll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll1lll1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll11l11l_opy_
    global bstack1ll1l1ll1l_opy_
    global bstack111lll1ll_opy_
    global bstack1ll11l1l11_opy_
    global bstack11ll1l1lll_opy_
    CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ૨")] = str(bstack11ll1l1lll_opy_) + str(__version__)
    bstack1l111l11_opy_ = os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૩")]
    bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(CONFIG, bstack11ll1l1lll_opy_)
    CONFIG[bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ૪")] = bstack1l111l11_opy_
    CONFIG[bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૫")] = bstack1l11ll1ll_opy_
    bstack11l111lll_opy_ = 0 if bstack1ll11l11l_opy_ < 0 else bstack1ll11l11l_opy_
    try:
      if bstack111lll1ll_opy_ is True:
        bstack11l111lll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11l1l11_opy_ is True:
        bstack11l111lll_opy_ = int(threading.current_thread().name)
    except:
      bstack11l111lll_opy_ = 0
    CONFIG[bstack111l1ll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ૬")] = True
    bstack1lll111ll_opy_ = bstack1ll11l1l_opy_(CONFIG, bstack11l111lll_opy_)
    logger.debug(bstack1llll11l_opy_.format(str(bstack1lll111ll_opy_)))
    if CONFIG.get(bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ૭")):
      bstack1l111l1111_opy_(bstack1lll111ll_opy_)
    if bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૮") in CONFIG and bstack111l1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ૯") in CONFIG[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૰")][bstack11l111lll_opy_]:
      bstack1ll1l1ll1l_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૱")][bstack11l111lll_opy_][bstack111l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ૲")]
    import urllib
    import json
    if bstack111l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ૳") in CONFIG and str(CONFIG[bstack111l1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૴")]).lower() != bstack111l1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ૵"):
        bstack1l1l111l11_opy_ = bstack1l1111llll_opy_()
        bstack111l111l_opy_ = bstack1l1l111l11_opy_ + urllib.parse.quote(json.dumps(bstack1lll111ll_opy_))
    else:
        bstack111l111l_opy_ = bstack111l1ll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ૶") + urllib.parse.quote(json.dumps(bstack1lll111ll_opy_))
    browser = self.connect(bstack111l111l_opy_)
    return browser
except Exception as e:
    pass
def bstack11l1l1l1_opy_():
    global bstack1l111l1l11_opy_
    global bstack11ll1l1lll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11lll1l11l_opy_
        global bstack1ll11lll_opy_
        if not bstack1ll1ll11l_opy_:
          global bstack111lllll_opy_
          if not bstack111lllll_opy_:
            from bstack_utils.helper import bstack1ll1l1111_opy_, bstack1ll1llll11_opy_, bstack11111l11_opy_
            bstack111lllll_opy_ = bstack1ll1l1111_opy_()
            bstack1ll1llll11_opy_(bstack11ll1l1lll_opy_)
            bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(CONFIG, bstack11ll1l1lll_opy_)
            bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ૷"), bstack1l11ll1ll_opy_)
          BrowserType.connect = bstack11lll1l11l_opy_
          return
        BrowserType.launch = bstack11lll1lll1_opy_
        bstack1l111l1l11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll1l1111_opy_
      bstack1l111l1l11_opy_ = True
    except Exception as e:
      pass
def bstack1lll1lll1l_opy_(context, bstack1l11l1l111_opy_):
  try:
    context.page.evaluate(bstack111l1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ૸"), bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ૹ")+ json.dumps(bstack1l11l1l111_opy_) + bstack111l1ll_opy_ (u"ࠥࢁࢂࠨૺ"))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤૻ"), e)
def bstack11l1l111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨૼ"), bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૽") + json.dumps(message) + bstack111l1ll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ૾") + json.dumps(level) + bstack111l1ll_opy_ (u"ࠨࡿࢀࠫ૿"))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ଀"), e)
@measure(event_name=EVENTS.bstack1l1l1l1lll_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack111111ll_opy_(self, url):
  global bstack1l11ll11l_opy_
  try:
    bstack1l1l1lll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11l11ll_opy_.format(str(err)))
  try:
    bstack1l11ll11l_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1111ll1l_opy_ = str(e)
      if any(err_msg in bstack1l1111ll1l_opy_ for err_msg in bstack11l1l11l_opy_):
        bstack1l1l1lll1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l11l11ll_opy_.format(str(err)))
    raise e
def bstack1l1l1111l_opy_(self):
  global bstack1l1l1l1l_opy_
  bstack1l1l1l1l_opy_ = self
  return
def bstack11ll111l1l_opy_(self):
  global bstack1ll1l111l1_opy_
  bstack1ll1l111l1_opy_ = self
  return
def bstack1l11l1111l_opy_(test_name, bstack111l1l11_opy_):
  global CONFIG
  if percy.bstack1l1l111ll1_opy_() == bstack111l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣଁ"):
    bstack1ll1111l_opy_ = os.path.relpath(bstack111l1l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll1111l_opy_)
    bstack11l1111ll_opy_ = suite_name + bstack111l1ll_opy_ (u"ࠦ࠲ࠨଂ") + test_name
    threading.current_thread().percySessionName = bstack11l1111ll_opy_
def bstack11l111111_opy_(self, test, *args, **kwargs):
  global bstack11l1l11l1_opy_
  test_name = None
  bstack111l1l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack111l1l11_opy_ = str(test.source)
  bstack1l11l1111l_opy_(test_name, bstack111l1l11_opy_)
  bstack11l1l11l1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1lll111lll_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack11ll1lll11_opy_(driver, bstack11l1111ll_opy_):
  if not bstack1ll11l1l1l_opy_ and bstack11l1111ll_opy_:
      bstack111l1111_opy_ = {
          bstack111l1ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଃ"): bstack111l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ଄"),
          bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଅ"): {
              bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ଆ"): bstack11l1111ll_opy_
          }
      }
      bstack1l1l1lllll_opy_ = bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧଇ").format(json.dumps(bstack111l1111_opy_))
      driver.execute_script(bstack1l1l1lllll_opy_)
  if bstack11l111l1l_opy_:
      bstack111l11l1l_opy_ = {
          bstack111l1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଈ"): bstack111l1ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ଉ"),
          bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଊ"): {
              bstack111l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫଋ"): bstack11l1111ll_opy_ + bstack111l1ll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩଌ"),
              bstack111l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ଍"): bstack111l1ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ଎")
          }
      }
      if bstack11l111l1l_opy_.status == bstack111l1ll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨଏ"):
          bstack11lllll1l_opy_ = bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩଐ").format(json.dumps(bstack111l11l1l_opy_))
          driver.execute_script(bstack11lllll1l_opy_)
          bstack11l1lllll1_opy_(driver, bstack111l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ଑"))
      elif bstack11l111l1l_opy_.status == bstack111l1ll_opy_ (u"࠭ࡆࡂࡋࡏࠫ଒"):
          reason = bstack111l1ll_opy_ (u"ࠢࠣଓ")
          bstack11l111l1_opy_ = bstack11l1111ll_opy_ + bstack111l1ll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩଔ")
          if bstack11l111l1l_opy_.message:
              reason = str(bstack11l111l1l_opy_.message)
              bstack11l111l1_opy_ = bstack11l111l1_opy_ + bstack111l1ll_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩକ") + reason
          bstack111l11l1l_opy_[bstack111l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଖ")] = {
              bstack111l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଗ"): bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫଘ"),
              bstack111l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫଙ"): bstack11l111l1_opy_
          }
          bstack11lllll1l_opy_ = bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬଚ").format(json.dumps(bstack111l11l1l_opy_))
          driver.execute_script(bstack11lllll1l_opy_)
          bstack11l1lllll1_opy_(driver, bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଛ"), reason)
          bstack1ll11111_opy_(reason, str(bstack11l111l1l_opy_), str(bstack1ll11l11l_opy_), logger)
@measure(event_name=EVENTS.bstack1lll11l11l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack11l1l1ll_opy_(driver, test):
  if percy.bstack1l1l111ll1_opy_() == bstack111l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢଜ") and percy.bstack1ll1111l11_opy_() == bstack111l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧଝ"):
      bstack1l111ll1ll_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧଞ"), None)
      bstack11ll1llll1_opy_(driver, bstack1l111ll1ll_opy_, test)
  if bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩଟ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬଠ"), None):
      logger.info(bstack111l1ll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢଡ"))
      bstack1l1llll111_opy_.bstack11lll1l1l1_opy_(driver, name=test.name, path=test.source)
def bstack11llll1l_opy_(test, bstack11l1111ll_opy_):
    try:
      data = {}
      if test:
        data[bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ଢ")] = bstack11l1111ll_opy_
      if bstack11l111l1l_opy_:
        if bstack11l111l1l_opy_.status == bstack111l1ll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧଣ"):
          data[bstack111l1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪତ")] = bstack111l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଥ")
        elif bstack11l111l1l_opy_.status == bstack111l1ll_opy_ (u"ࠬࡌࡁࡊࡎࠪଦ"):
          data[bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ଧ")] = bstack111l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧନ")
          if bstack11l111l1l_opy_.message:
            data[bstack111l1ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ଩")] = str(bstack11l111l1l_opy_.message)
      user = CONFIG[bstack111l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫପ")]
      key = CONFIG[bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ଫ")]
      url = bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩବ").format(user, key, bstack11ll1111l1_opy_)
      headers = {
        bstack111l1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫଭ"): bstack111l1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩମ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll111111l_opy_.format(str(e)))
def bstack1ll111ll11_opy_(test, bstack11l1111ll_opy_):
  global CONFIG
  global bstack1ll1l111l1_opy_
  global bstack1l1l1l1l_opy_
  global bstack11ll1111l1_opy_
  global bstack11l111l1l_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack1l1111ll_opy_
  global bstack1l11ll1l1_opy_
  global bstack1lll1l111_opy_
  global bstack1lll1l11l_opy_
  global bstack1ll1ll11ll_opy_
  global bstack11ll1ll11l_opy_
  try:
    if not bstack11ll1111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠧࡿࠩଯ")), bstack111l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨର"), bstack111l1ll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ଱"))) as f:
        bstack1l111l11l_opy_ = json.loads(bstack111l1ll_opy_ (u"ࠥࡿࠧଲ") + f.read().strip() + bstack111l1ll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ଳ") + bstack111l1ll_opy_ (u"ࠧࢃࠢ଴"))
        bstack11ll1111l1_opy_ = bstack1l111l11l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1ll11ll_opy_:
    for driver in bstack1ll1ll11ll_opy_:
      if bstack11ll1111l1_opy_ == driver.session_id:
        if test:
          bstack11l1l1ll_opy_(driver, test)
        bstack11ll1lll11_opy_(driver, bstack11l1111ll_opy_)
  elif bstack11ll1111l1_opy_:
    bstack11llll1l_opy_(test, bstack11l1111ll_opy_)
  if bstack1ll1l111l1_opy_:
    bstack1l11ll1l1_opy_(bstack1ll1l111l1_opy_)
  if bstack1l1l1l1l_opy_:
    bstack1lll1l111_opy_(bstack1l1l1l1l_opy_)
  if bstack11lll1ll_opy_:
    bstack1lll1l11l_opy_()
def bstack1l1l1lll11_opy_(self, test, *args, **kwargs):
  bstack11l1111ll_opy_ = None
  if test:
    bstack11l1111ll_opy_ = str(test.name)
  bstack1ll111ll11_opy_(test, bstack11l1111ll_opy_)
  bstack1l1111ll_opy_(self, test, *args, **kwargs)
def bstack11ll11lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1lll1_opy_
  global CONFIG
  global bstack1ll1ll11ll_opy_
  global bstack11ll1111l1_opy_
  bstack1l1llllll1_opy_ = None
  try:
    if bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬଵ"), None):
      try:
        if not bstack11ll1111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠧࡿࠩଶ")), bstack111l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଷ"), bstack111l1ll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫସ"))) as f:
            bstack1l111l11l_opy_ = json.loads(bstack111l1ll_opy_ (u"ࠥࡿࠧହ") + f.read().strip() + bstack111l1ll_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭଺") + bstack111l1ll_opy_ (u"ࠧࢃࠢ଻"))
            bstack11ll1111l1_opy_ = bstack1l111l11l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1ll11ll_opy_:
        for driver in bstack1ll1ll11ll_opy_:
          if bstack11ll1111l1_opy_ == driver.session_id:
            bstack1l1llllll1_opy_ = driver
    bstack11lll1111_opy_ = bstack1l1llll111_opy_.bstack1llll1ll1l_opy_(test.tags)
    if bstack1l1llllll1_opy_:
      threading.current_thread().isA11yTest = bstack1l1llll111_opy_.bstack11ll111l1_opy_(bstack1l1llllll1_opy_, bstack11lll1111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11lll1111_opy_
  except:
    pass
  bstack11ll1lll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l111l1l_opy_
  try:
    bstack11l111l1l_opy_ = self._test
  except:
    bstack11l111l1l_opy_ = self.test
def bstack1l1l1l1l1l_opy_():
  global bstack1ll1ll111_opy_
  try:
    if os.path.exists(bstack1ll1ll111_opy_):
      os.remove(bstack1ll1ll111_opy_)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺଼ࠡࠩ") + str(e))
def bstack1l1l1l11_opy_():
  global bstack1ll1ll111_opy_
  bstack111111l1_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll1ll111_opy_):
      with open(bstack1ll1ll111_opy_, bstack111l1ll_opy_ (u"ࠧࡸࠩଽ")):
        pass
      with open(bstack1ll1ll111_opy_, bstack111l1ll_opy_ (u"ࠣࡹ࠮ࠦା")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll1ll111_opy_):
      bstack111111l1_opy_ = json.load(open(bstack1ll1ll111_opy_, bstack111l1ll_opy_ (u"ࠩࡵࡦࠬି")))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬୀ") + str(e))
  finally:
    return bstack111111l1_opy_
def bstack111ll11l_opy_(platform_index, item_index):
  global bstack1ll1ll111_opy_
  try:
    bstack111111l1_opy_ = bstack1l1l1l11_opy_()
    bstack111111l1_opy_[item_index] = platform_index
    with open(bstack1ll1ll111_opy_, bstack111l1ll_opy_ (u"ࠦࡼ࠱ࠢୁ")) as outfile:
      json.dump(bstack111111l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪୂ") + str(e))
def bstack1l11l11111_opy_(bstack1l111lll11_opy_):
  global CONFIG
  bstack1lll111ll1_opy_ = bstack111l1ll_opy_ (u"࠭ࠧୃ")
  if not bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୄ") in CONFIG:
    logger.info(bstack111l1ll_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ୅"))
  try:
    platform = CONFIG[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୆")][bstack1l111lll11_opy_]
    if bstack111l1ll_opy_ (u"ࠪࡳࡸ࠭େ") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"ࠫࡴࡹࠧୈ")]) + bstack111l1ll_opy_ (u"ࠬ࠲ࠠࠨ୉")
    if bstack111l1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ୊") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪୋ")]) + bstack111l1ll_opy_ (u"ࠨ࠮ࠣࠫୌ")
    if bstack111l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ୍࠭") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ୎")]) + bstack111l1ll_opy_ (u"ࠫ࠱ࠦࠧ୏")
    if bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ୐") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୑")]) + bstack111l1ll_opy_ (u"ࠧ࠭ࠢࠪ୒")
    if bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୓") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୔")]) + bstack111l1ll_opy_ (u"ࠪ࠰ࠥ࠭୕")
    if bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬୖ") in platform:
      bstack1lll111ll1_opy_ += str(platform[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ୗ")]) + bstack111l1ll_opy_ (u"࠭ࠬࠡࠩ୘")
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧ୙") + str(e))
  finally:
    if bstack1lll111ll1_opy_[len(bstack1lll111ll1_opy_) - 2:] == bstack111l1ll_opy_ (u"ࠨ࠮ࠣࠫ୚"):
      bstack1lll111ll1_opy_ = bstack1lll111ll1_opy_[:-2]
    return bstack1lll111ll1_opy_
def bstack1llll1l1_opy_(path, bstack1lll111ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1llllllll_opy_ = ET.parse(path)
    bstack111ll11ll_opy_ = bstack1llllllll_opy_.getroot()
    bstack111lll1l1_opy_ = None
    for suite in bstack111ll11ll_opy_.iter(bstack111l1ll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ୛")):
      if bstack111l1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪଡ଼") in suite.attrib:
        suite.attrib[bstack111l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩଢ଼")] += bstack111l1ll_opy_ (u"ࠬࠦࠧ୞") + bstack1lll111ll1_opy_
        bstack111lll1l1_opy_ = suite
    bstack1l1ll1lll1_opy_ = None
    for robot in bstack111ll11ll_opy_.iter(bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬୟ")):
      bstack1l1ll1lll1_opy_ = robot
    bstack11llll11_opy_ = len(bstack1l1ll1lll1_opy_.findall(bstack111l1ll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ୠ")))
    if bstack11llll11_opy_ == 1:
      bstack1l1ll1lll1_opy_.remove(bstack1l1ll1lll1_opy_.findall(bstack111l1ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧୡ"))[0])
      bstack1lll111l_opy_ = ET.Element(bstack111l1ll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨୢ"), attrib={bstack111l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨୣ"): bstack111l1ll_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ୤"), bstack111l1ll_opy_ (u"ࠬ࡯ࡤࠨ୥"): bstack111l1ll_opy_ (u"࠭ࡳ࠱ࠩ୦")})
      bstack1l1ll1lll1_opy_.insert(1, bstack1lll111l_opy_)
      bstack1l1l1llll_opy_ = None
      for suite in bstack1l1ll1lll1_opy_.iter(bstack111l1ll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭୧")):
        bstack1l1l1llll_opy_ = suite
      bstack1l1l1llll_opy_.append(bstack111lll1l1_opy_)
      bstack1ll11lll11_opy_ = None
      for status in bstack111lll1l1_opy_.iter(bstack111l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୨")):
        bstack1ll11lll11_opy_ = status
      bstack1l1l1llll_opy_.append(bstack1ll11lll11_opy_)
    bstack1llllllll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ୩") + str(e))
def bstack11lll1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111l11l11_opy_
  global CONFIG
  if bstack111l1ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ୪") in options:
    del options[bstack111l1ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ୫")]
  bstack11ll11l111_opy_ = bstack1l1l1l11_opy_()
  for bstack11l11111l_opy_ in bstack11ll11l111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬ୬"), str(bstack11l11111l_opy_), bstack111l1ll_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪ୭"))
    bstack1llll1l1_opy_(path, bstack1l11l11111_opy_(bstack11ll11l111_opy_[bstack11l11111l_opy_]))
  bstack1l1l1l1l1l_opy_()
  return bstack111l11l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11ll11ll1l_opy_(self, ff_profile_dir):
  global bstack1l111l11ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l111l11ll_opy_(self, ff_profile_dir)
def bstack11llllll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1ll1l11l_opy_
  bstack1lll11lll1_opy_ = []
  if bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୮") in CONFIG:
    bstack1lll11lll1_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୯")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l1ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ୰")],
      pabot_args[bstack111l1ll_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦୱ")],
      argfile,
      pabot_args.get(bstack111l1ll_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ୲")),
      pabot_args[bstack111l1ll_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ୳")],
      platform[0],
      bstack1l1ll1l11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l1ll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ୴")] or [(bstack111l1ll_opy_ (u"ࠢࠣ୵"), None)]
    for platform in enumerate(bstack1lll11lll1_opy_)
  ]
def bstack1l11l1l11l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11lll11111_opy_=bstack111l1ll_opy_ (u"ࠨࠩ୶")):
  global bstack11llll1l1_opy_
  self.platform_index = platform_index
  self.bstack1ll11l1lll_opy_ = bstack11lll11111_opy_
  bstack11llll1l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1lll1l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1ll1111_opy_
  global bstack1ll111l1ll_opy_
  bstack1l11ll1l11_opy_ = copy.deepcopy(item)
  if not bstack111l1ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୷") in item.options:
    bstack1l11ll1l11_opy_.options[bstack111l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୸")] = []
  bstack1ll11l1111_opy_ = bstack1l11ll1l11_opy_.options[bstack111l1ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭୹")].copy()
  for v in bstack1l11ll1l11_opy_.options[bstack111l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ୺")]:
    if bstack111l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ୻") in v:
      bstack1ll11l1111_opy_.remove(v)
    if bstack111l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ୼") in v:
      bstack1ll11l1111_opy_.remove(v)
    if bstack111l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ୽") in v:
      bstack1ll11l1111_opy_.remove(v)
  bstack1ll11l1111_opy_.insert(0, bstack111l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ୾").format(bstack1l11ll1l11_opy_.platform_index))
  bstack1ll11l1111_opy_.insert(0, bstack111l1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ୿").format(bstack1l11ll1l11_opy_.bstack1ll11l1lll_opy_))
  bstack1l11ll1l11_opy_.options[bstack111l1ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭஀")] = bstack1ll11l1111_opy_
  if bstack1ll111l1ll_opy_:
    bstack1l11ll1l11_opy_.options[bstack111l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ஁")].insert(0, bstack111l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩஂ").format(bstack1ll111l1ll_opy_))
  return bstack1l1ll1111_opy_(caller_id, datasources, is_last, bstack1l11ll1l11_opy_, outs_dir)
def bstack1ll111l1l1_opy_(command, item_index):
  if bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨஃ")):
    os.environ[bstack111l1ll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ஄")] = json.dumps(CONFIG[bstack111l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬஅ")][item_index % bstack1lll1l1ll_opy_])
  global bstack1ll111l1ll_opy_
  if bstack1ll111l1ll_opy_:
    command[0] = command[0].replace(bstack111l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩஆ"), bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨஇ") + str(
      item_index) + bstack111l1ll_opy_ (u"ࠬࠦࠧஈ") + bstack1ll111l1ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஉ"),
                                    bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫஊ") + str(item_index), 1)
def bstack1l1lll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1ll1ll1_opy_
  bstack1ll111l1l1_opy_(command, item_index)
  return bstack1l1ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1lll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1ll1ll1_opy_
  bstack1ll111l1l1_opy_(command, item_index)
  return bstack1l1ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11l1l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1ll1ll1_opy_
  bstack1ll111l1l1_opy_(command, item_index)
  return bstack1l1ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1l1ll111_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11111ll1_opy_
  bstack1ll11lllll_opy_ = bstack1l11111ll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l1ll_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨ஋")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l1ll_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭஌")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll11lllll_opy_
def bstack11lllll111_opy_(runner, hook_name, context, element, bstack1l11l111l1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l11l1l1_opy_.bstack11ll111lll_opy_(hook_name, element)
    bstack1l11l111l1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l11l1l1_opy_.bstack1l111l1l1l_opy_(element)
      if hook_name not in [bstack111l1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ஍"), bstack111l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧஎ")] and args and hasattr(args[0], bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬஏ")):
        args[0].error_message = bstack111l1ll_opy_ (u"࠭ࠧஐ")
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ஑").format(str(e)))
@measure(event_name=EVENTS.bstack1l11llll1_opy_, stage=STAGE.SINGLE, hook_type=bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦஒ"), bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1111ll11l_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    if runner.hooks.get(bstack111l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨஓ")).__name__ != bstack111l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨஔ"):
      bstack11lllll111_opy_(runner, name, context, runner, bstack1l11l111l1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l11ll1_opy_(bstack111l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪக")) else context.browser
      runner.driver_initialised = bstack111l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ஖")
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪ஗").format(str(e)))
def bstack1l11111ll_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    bstack11lllll111_opy_(runner, name, context, context.feature, bstack1l11l111l1_opy_, *args)
    try:
      if not bstack1ll11l1l1l_opy_:
        bstack1l1llllll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll1_opy_(bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭஘")) else context.browser
        if is_driver_active(bstack1l1llllll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤங")
          bstack1l11l1l111_opy_ = str(runner.feature.name)
          bstack1lll1lll1l_opy_(context, bstack1l11l1l111_opy_)
          bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧச") + json.dumps(bstack1l11l1l111_opy_) + bstack111l1ll_opy_ (u"ࠪࢁࢂ࠭஛"))
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫஜ").format(str(e)))
def bstack1l1111111l_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    if hasattr(context, bstack111l1ll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ஝")):
        bstack1l11l1l1_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111l1ll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨஞ")) else context.feature
    bstack11lllll111_opy_(runner, name, context, target, bstack1l11l111l1_opy_, *args)
@measure(event_name=EVENTS.bstack1lll1l1l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack11lll11lll_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l11l1l1_opy_.start_test(context)
    bstack11lllll111_opy_(runner, name, context, context.scenario, bstack1l11l111l1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11ll1111ll_opy_.bstack1ll1l11111_opy_(context, *args)
    try:
      bstack1l1llllll1_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ட"), context.browser)
      if is_driver_active(bstack1l1llllll1_opy_):
        bstack1lll1ll111_opy_.bstack1lllll1lll_opy_(bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ஠"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ஡")
        if (not bstack1ll11l1l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l11l1l111_opy_ = str(runner.feature.name)
          bstack1l11l1l111_opy_ = feature_name + bstack111l1ll_opy_ (u"ࠪࠤ࠲ࠦࠧ஢") + scenario_name
          if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨண"):
            bstack1lll1lll1l_opy_(context, bstack1l11l1l111_opy_)
            bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪத") + json.dumps(bstack1l11l1l111_opy_) + bstack111l1ll_opy_ (u"࠭ࡽࡾࠩ஥"))
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ஦").format(str(e)))
@measure(event_name=EVENTS.bstack1l11llll1_opy_, stage=STAGE.SINGLE, hook_type=bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡔࡶࡨࡴࠧ஧"), bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1ll1l1l111_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    bstack11lllll111_opy_(runner, name, context, args[0], bstack1l11l111l1_opy_, *args)
    try:
      bstack1l1llllll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll1_opy_(bstack111l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨந")) else context.browser
      if is_driver_active(bstack1l1llllll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣன")
        bstack1l11l1l1_opy_.bstack111ll1l1_opy_(args[0])
        if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤப"):
          feature_name = bstack1l11l1l111_opy_ = str(runner.feature.name)
          bstack1l11l1l111_opy_ = feature_name + bstack111l1ll_opy_ (u"ࠬࠦ࠭ࠡࠩ஫") + context.scenario.name
          bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ஬") + json.dumps(bstack1l11l1l111_opy_) + bstack111l1ll_opy_ (u"ࠧࡾࡿࠪ஭"))
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬம").format(str(e)))
@measure(event_name=EVENTS.bstack1l11llll1_opy_, stage=STAGE.SINGLE, hook_type=bstack111l1ll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡔࡶࡨࡴࠧய"), bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1l1l11l1_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
  bstack1l11l1l1_opy_.bstack1l1l11ll11_opy_(args[0])
  try:
    bstack1llllll1l1_opy_ = args[0].status.name
    bstack1l1llllll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩர") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1llllll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111l1ll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫற")
        feature_name = bstack1l11l1l111_opy_ = str(runner.feature.name)
        bstack1l11l1l111_opy_ = feature_name + bstack111l1ll_opy_ (u"ࠬࠦ࠭ࠡࠩல") + context.scenario.name
        bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫள") + json.dumps(bstack1l11l1l111_opy_) + bstack111l1ll_opy_ (u"ࠧࡾࡿࠪழ"))
    if str(bstack1llllll1l1_opy_).lower() == bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨவ"):
      bstack111l1lll1_opy_ = bstack111l1ll_opy_ (u"ࠩࠪஶ")
      bstack1l11l1ll1_opy_ = bstack111l1ll_opy_ (u"ࠪࠫஷ")
      bstack1ll1ll11l1_opy_ = bstack111l1ll_opy_ (u"ࠫࠬஸ")
      try:
        import traceback
        bstack111l1lll1_opy_ = runner.exception.__class__.__name__
        bstack1ll1l111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11l1ll1_opy_ = bstack111l1ll_opy_ (u"ࠬࠦࠧஹ").join(bstack1ll1l111l_opy_)
        bstack1ll1ll11l1_opy_ = bstack1ll1l111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1llll1l_opy_.format(str(e)))
      bstack111l1lll1_opy_ += bstack1ll1ll11l1_opy_
      bstack11l1l111_opy_(context, json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ஺") + str(bstack1l11l1ll1_opy_)),
                          bstack111l1ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ஻"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ஼"):
        bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ஽"), None), bstack111l1ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥா"), bstack111l1lll1_opy_)
        bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩி") + json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦீ") + str(bstack1l11l1ll1_opy_)) + bstack111l1ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ு"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧூ"):
        bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௃"), bstack111l1ll_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ௄") + str(bstack111l1lll1_opy_))
    else:
      bstack11l1l111_opy_(context, bstack111l1ll_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ௅"), bstack111l1ll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤெ"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥே"):
        bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"࠭ࡰࡢࡩࡨࠫை"), None), bstack111l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ௉"))
      bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ொ") + json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨோ")) + bstack111l1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩௌ"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ்"):
        bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ௎"))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ௏").format(str(e)))
  bstack11lllll111_opy_(runner, name, context, args[0], bstack1l11l111l1_opy_, *args)
@measure(event_name=EVENTS.bstack11l1111l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1111l11l1_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
  bstack1l11l1l1_opy_.end_test(args[0])
  try:
    bstack111l1ll1_opy_ = args[0].status.name
    bstack1l1llllll1_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ௐ"), context.browser)
    bstack11ll1111ll_opy_.bstack11l1l1l1l_opy_(bstack1l1llllll1_opy_)
    if str(bstack111l1ll1_opy_).lower() == bstack111l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௑"):
      bstack111l1lll1_opy_ = bstack111l1ll_opy_ (u"ࠩࠪ௒")
      bstack1l11l1ll1_opy_ = bstack111l1ll_opy_ (u"ࠪࠫ௓")
      bstack1ll1ll11l1_opy_ = bstack111l1ll_opy_ (u"ࠫࠬ௔")
      try:
        import traceback
        bstack111l1lll1_opy_ = runner.exception.__class__.__name__
        bstack1ll1l111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11l1ll1_opy_ = bstack111l1ll_opy_ (u"ࠬࠦࠧ௕").join(bstack1ll1l111l_opy_)
        bstack1ll1ll11l1_opy_ = bstack1ll1l111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1llll1l_opy_.format(str(e)))
      bstack111l1lll1_opy_ += bstack1ll1ll11l1_opy_
      bstack11l1l111_opy_(context, json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ௖") + str(bstack1l11l1ll1_opy_)),
                          bstack111l1ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨௗ"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௘") or runner.driver_initialised == bstack111l1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ௙"):
        bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ௚"), None), bstack111l1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ௛"), bstack111l1lll1_opy_)
        bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ௜") + json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ௝") + str(bstack1l11l1ll1_opy_)) + bstack111l1ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ௞"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௟") or runner.driver_initialised == bstack111l1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ௠"):
        bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ௡"), bstack111l1ll_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ௢") + str(bstack111l1lll1_opy_))
    else:
      bstack11l1l111_opy_(context, bstack111l1ll_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ௣"), bstack111l1ll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ௤"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௥") or runner.driver_initialised == bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ௦"):
        bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௧"), None), bstack111l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ௨"))
      bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௩") + json.dumps(str(args[0].name) + bstack111l1ll_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ௪")) + bstack111l1ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௫"))
      if runner.driver_initialised == bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௬") or runner.driver_initialised == bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ௭"):
        bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ௮"))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ௯").format(str(e)))
  bstack11lllll111_opy_(runner, name, context, context.scenario, bstack1l11l111l1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1lllll1l_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack111l1ll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭௰")) else context.feature
    bstack11lllll111_opy_(runner, name, context, target, bstack1l11l111l1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l111llll_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    try:
      bstack1l1llllll1_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ௱"), context.browser)
      bstack11lll1l1l_opy_ = bstack111l1ll_opy_ (u"࠭ࠧ௲")
      if context.failed is True:
        bstack11lll1111l_opy_ = []
        bstack11ll1l111l_opy_ = []
        bstack1ll1l11l1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lll1111l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll1l111l_opy_ = traceback.format_tb(exc_tb)
            bstack11111llll_opy_ = bstack111l1ll_opy_ (u"ࠧࠡࠩ௳").join(bstack1ll1l111l_opy_)
            bstack11ll1l111l_opy_.append(bstack11111llll_opy_)
            bstack1ll1l11l1_opy_.append(bstack1ll1l111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1llll1l_opy_.format(str(e)))
        bstack111l1lll1_opy_ = bstack111l1ll_opy_ (u"ࠨࠩ௴")
        for i in range(len(bstack11lll1111l_opy_)):
          bstack111l1lll1_opy_ += bstack11lll1111l_opy_[i] + bstack1ll1l11l1_opy_[i] + bstack111l1ll_opy_ (u"ࠩ࡟ࡲࠬ௵")
        bstack11lll1l1l_opy_ = bstack111l1ll_opy_ (u"ࠪࠤࠬ௶").join(bstack11ll1l111l_opy_)
        if runner.driver_initialised in [bstack111l1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ௷"), bstack111l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ௸")]:
          bstack11l1l111_opy_(context, bstack11lll1l1l_opy_, bstack111l1ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ௹"))
          bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬ௺"), None), bstack111l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ௻"), bstack111l1lll1_opy_)
          bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ௼") + json.dumps(bstack11lll1l1l_opy_) + bstack111l1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ௽"))
          bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ௾"), bstack111l1ll_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥ௿") + str(bstack111l1lll1_opy_))
          bstack1l1l11ll1_opy_ = bstack11111l1l1_opy_(bstack11lll1l1l_opy_, runner.feature.name, logger)
          if (bstack1l1l11ll1_opy_ != None):
            bstack1ll1llllll_opy_.append(bstack1l1l11ll1_opy_)
      else:
        if runner.driver_initialised in [bstack111l1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢఀ"), bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦఁ")]:
          bstack11l1l111_opy_(context, bstack111l1ll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦం") + str(runner.feature.name) + bstack111l1ll_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦః"), bstack111l1ll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣఄ"))
          bstack11ll111l11_opy_(getattr(context, bstack111l1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩఅ"), None), bstack111l1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧఆ"))
          bstack1l1llllll1_opy_.execute_script(bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫఇ") + json.dumps(bstack111l1ll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥఈ") + str(runner.feature.name) + bstack111l1ll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥఉ")) + bstack111l1ll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨఊ"))
          bstack11l1lllll1_opy_(bstack1l1llllll1_opy_, bstack111l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪఋ"))
          bstack1l1l11ll1_opy_ = bstack11111l1l1_opy_(bstack11lll1l1l_opy_, runner.feature.name, logger)
          if (bstack1l1l11ll1_opy_ != None):
            bstack1ll1llllll_opy_.append(bstack1l1l11ll1_opy_)
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ఌ").format(str(e)))
    bstack11lllll111_opy_(runner, name, context, context.feature, bstack1l11l111l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l11llll1_opy_, stage=STAGE.SINGLE, hook_type=bstack111l1ll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡅࡱࡲࠢ఍"), bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack11ll1l1l_opy_(runner, name, context, bstack1l11l111l1_opy_, *args):
    bstack11lllll111_opy_(runner, name, context, runner, bstack1l11l111l1_opy_, *args)
def bstack1l1lll1lll_opy_(self, name, context, *args):
  if bstack1ll1ll11l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1lll1l1ll_opy_
    bstack1l1l11111_opy_ = CONFIG[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఎ")][platform_index]
    os.environ[bstack111l1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨఏ")] = json.dumps(bstack1l1l11111_opy_)
  global bstack1l11l111l1_opy_
  if not hasattr(self, bstack111l1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࡩ࠭ఐ")):
    self.driver_initialised = None
  bstack1ll11ll1ll_opy_ = {
      bstack111l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭఑"): bstack1111ll11l_opy_,
      bstack111l1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫఒ"): bstack1l11111ll_opy_,
      bstack111l1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨఓ"): bstack1l1111111l_opy_,
      bstack111l1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧఔ"): bstack11lll11lll_opy_,
      bstack111l1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠫక"): bstack1ll1l1l111_opy_,
      bstack111l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫఖ"): bstack1l1l11l1_opy_,
      bstack111l1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩగ"): bstack1111l11l1_opy_,
      bstack111l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡶࡤ࡫ࠬఘ"): bstack1l1lllll1l_opy_,
      bstack111l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪఙ"): bstack1l111llll_opy_,
      bstack111l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧచ"): bstack11ll1l1l_opy_
  }
  handler = bstack1ll11ll1ll_opy_.get(name, bstack1l11l111l1_opy_)
  handler(self, name, context, bstack1l11l111l1_opy_, *args)
  if name in [bstack111l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬఛ"), bstack111l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧజ"), bstack111l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪఝ")]:
    try:
      bstack1l1llllll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11ll1_opy_(bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఞ")) else context.browser
      bstack11ll11ll_opy_ = (
        (name == bstack111l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬట") and self.driver_initialised == bstack111l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢఠ")) or
        (name == bstack111l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫడ") and self.driver_initialised == bstack111l1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨఢ")) or
        (name == bstack111l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧణ") and self.driver_initialised in [bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤత"), bstack111l1ll_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣథ")]) or
        (name == bstack111l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭ద") and self.driver_initialised == bstack111l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣధ"))
      )
      if bstack11ll11ll_opy_:
        self.driver_initialised = None
        bstack1l1llllll1_opy_.quit()
    except Exception:
      pass
def bstack1111l111_opy_(config, startdir):
  return bstack111l1ll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤన").format(bstack111l1ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ఩"))
notset = Notset()
def bstack11lll1l111_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll11l111_opy_
  if str(name).lower() == bstack111l1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ప"):
    return bstack111l1ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨఫ")
  else:
    return bstack1ll11l111_opy_(self, name, default, skip)
def bstack1l1llll11l_opy_(item, when):
  global bstack1llll11ll_opy_
  try:
    bstack1llll11ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l111lll_opy_():
  return
def bstack1l1l1ll1l1_opy_(type, name, status, reason, bstack1ll11l111l_opy_, bstack1llll11l11_opy_):
  bstack111l1111_opy_ = {
    bstack111l1ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨబ"): type,
    bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬభ"): {}
  }
  if type == bstack111l1ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬమ"):
    bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧయ")][bstack111l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫర")] = bstack1ll11l111l_opy_
    bstack111l1111_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩఱ")][bstack111l1ll_opy_ (u"ࠧࡥࡣࡷࡥࠬల")] = json.dumps(str(bstack1llll11l11_opy_))
  if type == bstack111l1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩళ"):
    bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬఴ")][bstack111l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨవ")] = name
  if type == bstack111l1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧశ"):
    bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨష")][bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭స")] = status
    if status == bstack111l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧహ"):
      bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ఺")][bstack111l1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ఻")] = json.dumps(str(reason))
  bstack1l1l1lllll_opy_ = bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ఼").format(json.dumps(bstack111l1111_opy_))
  return bstack1l1l1lllll_opy_
def bstack11l11llll_opy_(driver_command, response):
    if driver_command == bstack111l1ll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨఽ"):
        bstack1lll1ll111_opy_.bstack1111lll1l_opy_({
            bstack111l1ll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫా"): response[bstack111l1ll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬి")],
            bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧీ"): bstack1lll1ll111_opy_.current_test_uuid()
        })
def bstack1lll11l1l1_opy_(item, call, rep):
  global bstack1llll1ll_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1ll11l1l1l_opy_
  name = bstack111l1ll_opy_ (u"ࠨࠩు")
  try:
    if rep.when == bstack111l1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧూ"):
      bstack11ll1111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11l1l1l_opy_:
          name = str(rep.nodeid)
          bstack1lll11l1l_opy_ = bstack1l1l1ll1l1_opy_(bstack111l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫృ"), name, bstack111l1ll_opy_ (u"ࠫࠬౄ"), bstack111l1ll_opy_ (u"ࠬ࠭౅"), bstack111l1ll_opy_ (u"࠭ࠧె"), bstack111l1ll_opy_ (u"ࠧࠨే"))
          threading.current_thread().bstack1ll1ll1l1_opy_ = name
          for driver in bstack1ll1ll11ll_opy_:
            if bstack11ll1111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11l1l_opy_)
      except Exception as e:
        logger.debug(bstack111l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨై").format(str(e)))
      try:
        bstack111l11111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ౉"):
          status = bstack111l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪొ") if rep.outcome.lower() == bstack111l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫో") else bstack111l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬౌ")
          reason = bstack111l1ll_opy_ (u"్࠭ࠧ")
          if status == bstack111l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౎"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭౏") if status == bstack111l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౐") else bstack111l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ౑")
          data = name + bstack111l1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭౒") if status == bstack111l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౓") else name + bstack111l1ll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ౔") + reason
          bstack1l11llllll_opy_ = bstack1l1l1ll1l1_opy_(bstack111l1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦౕࠩ"), bstack111l1ll_opy_ (u"ࠨౖࠩ"), bstack111l1ll_opy_ (u"ࠩࠪ౗"), bstack111l1ll_opy_ (u"ࠪࠫౘ"), level, data)
          for driver in bstack1ll1ll11ll_opy_:
            if bstack11ll1111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11llllll_opy_)
      except Exception as e:
        logger.debug(bstack111l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨౙ").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩౚ").format(str(e)))
  bstack1llll1ll_opy_(item, call, rep)
def bstack11ll1llll1_opy_(driver, bstack1lll111l1_opy_, test=None):
  global bstack1ll11l11l_opy_
  if test != None:
    bstack1l1l1111l1_opy_ = getattr(test, bstack111l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౛"), None)
    bstack1l1lll1l_opy_ = getattr(test, bstack111l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ౜"), None)
    PercySDK.screenshot(driver, bstack1lll111l1_opy_, bstack1l1l1111l1_opy_=bstack1l1l1111l1_opy_, bstack1l1lll1l_opy_=bstack1l1lll1l_opy_, bstack11l11l111_opy_=bstack1ll11l11l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1lll111l1_opy_)
@measure(event_name=EVENTS.bstack1l1l11lll_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1l111llll1_opy_(driver):
  if bstack11lllll1_opy_.bstack1lll1l111l_opy_() is True or bstack11lllll1_opy_.capturing() is True:
    return
  bstack11lllll1_opy_.bstack1ll1l1111l_opy_()
  while not bstack11lllll1_opy_.bstack1lll1l111l_opy_():
    bstack1l1l11l111_opy_ = bstack11lllll1_opy_.bstack11ll11lll1_opy_()
    bstack11ll1llll1_opy_(driver, bstack1l1l11l111_opy_)
  bstack11lllll1_opy_.bstack111llll11_opy_()
def bstack1lll1lllll_opy_(sequence, driver_command, response = None, bstack11111l1ll_opy_ = None, args = None):
    try:
      if sequence != bstack111l1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨౝ"):
        return
      if percy.bstack1l1l111ll1_opy_() == bstack111l1ll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ౞"):
        return
      bstack1l1l11l111_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౟"), None)
      for command in bstack1ll1l1llll_opy_:
        if command == driver_command:
          for driver in bstack1ll1ll11ll_opy_:
            bstack1l111llll1_opy_(driver)
      bstack1lll11111l_opy_ = percy.bstack1ll1111l11_opy_()
      if driver_command in bstack1l1l1ll11_opy_[bstack1lll11111l_opy_]:
        bstack11lllll1_opy_.bstack1l1l11l1l_opy_(bstack1l1l11l111_opy_, driver_command)
    except Exception as e:
      pass
@measure(event_name=EVENTS.bstack111lllll1_opy_, stage=STAGE.bstack1l1l1ll1_opy_)
def bstack1l1ll1ll1l_opy_(framework_name):
  if bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨౠ")):
      return
  bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩౡ"), True)
  global bstack11ll1l1lll_opy_
  global bstack1l111l1l11_opy_
  global bstack1llll111l1_opy_
  bstack11ll1l1lll_opy_ = framework_name
  logger.info(bstack1llll1111l_opy_.format(bstack11ll1l1lll_opy_.split(bstack111l1ll_opy_ (u"࠭࠭ࠨౢ"))[0]))
  bstack11ll1l1ll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1ll11l_opy_:
      Service.start = bstack111lll1l_opy_
      Service.stop = bstack1l1l11llll_opy_
      webdriver.Remote.get = bstack111111ll_opy_
      WebDriver.close = bstack1l111lll_opy_
      WebDriver.quit = bstack1llll11l1l_opy_
      webdriver.Remote.__init__ = bstack1l1lll1ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll1ll11l_opy_:
        webdriver.Remote.__init__ = bstack111l1l1l_opy_
    WebDriver.execute = bstack1ll11ll111_opy_
    bstack1l111l1l11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll1ll11l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll11l11_opy_
  except Exception as e:
    pass
  bstack11l1l1l1_opy_()
  if not bstack1l111l1l11_opy_:
    bstack1lll11ll_opy_(bstack111l1ll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤౣ"), bstack1l1lllll11_opy_)
  if bstack1l1llll1ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1l1111lll_opy_ = bstack1l11l111_opy_
    except Exception as e:
      logger.error(bstack1l11lll1ll_opy_.format(str(e)))
  if bstack1llll1lll_opy_():
    bstack1lll1l11ll_opy_(CONFIG, logger)
  if (bstack111l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ౤") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l1l111ll1_opy_() == bstack111l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ౥"):
          bstack1ll1l111_opy_(bstack1lll1lllll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11ll11ll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11ll111l1l_opy_
      except Exception as e:
        logger.warn(bstack1ll1lllll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1l1111l_opy_
      except Exception as e:
        logger.debug(bstack1ll1l1l11l_opy_ + str(e))
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll1_opy_)
    Output.start_test = bstack11l111111_opy_
    Output.end_test = bstack1l1l1lll11_opy_
    TestStatus.__init__ = bstack11ll11lll_opy_
    QueueItem.__init__ = bstack1l11l1l11l_opy_
    pabot._create_items = bstack11llllll11_opy_
    try:
      from pabot import __version__ as bstack11l11l1ll_opy_
      if version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack111l1ll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪ౦")):
        pabot._run = bstack11l1l1l11_opy_
      elif version.parse(bstack11l11l1ll_opy_) >= version.parse(bstack111l1ll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫ౧")):
        pabot._run = bstack1l1lll111l_opy_
      else:
        pabot._run = bstack1l1lll11ll_opy_
    except Exception as e:
      pabot._run = bstack1l1lll11ll_opy_
    pabot._create_command_for_execution = bstack1ll1lll1l1_opy_
    pabot._report_results = bstack11lll1l1ll_opy_
  if bstack111l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ౨") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll_opy_)
    Runner.run_hook = bstack1l1lll1lll_opy_
    Step.run = bstack1l1l1ll111_opy_
  if bstack111l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭౩") in str(framework_name).lower():
    if not bstack1ll1ll11l_opy_:
      return
    try:
      if percy.bstack1l1l111ll1_opy_() == bstack111l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ౪"):
          bstack1ll1l111_opy_(bstack1lll1lllll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1111l111_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l111lll_opy_
      Config.getoption = bstack11lll1l111_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll11l1l1_opy_
    except Exception as e:
      pass
def bstack11ll11l1ll_opy_():
  global CONFIG
  if bstack111l1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ౫") in CONFIG and int(CONFIG[bstack111l1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ౬")]) > 1:
    logger.warn(bstack11lll1llll_opy_)
def bstack11111ll1_opy_(arg, bstack11ll11l1l1_opy_, bstack1l1lll1ll1_opy_=None):
  global CONFIG
  global bstack1lll11l111_opy_
  global bstack11l11l1l_opy_
  global bstack1ll1ll11l_opy_
  global bstack1ll11lll_opy_
  bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౭")
  if bstack11ll11l1l1_opy_ and isinstance(bstack11ll11l1l1_opy_, str):
    bstack11ll11l1l1_opy_ = eval(bstack11ll11l1l1_opy_)
  CONFIG = bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ౮")]
  bstack1lll11l111_opy_ = bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭౯")]
  bstack11l11l1l_opy_ = bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ౰")]
  bstack1ll1ll11l_opy_ = bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ౱")]
  bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ౲"), bstack1ll1ll11l_opy_)
  os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ౳")] = bstack11lll1lll_opy_
  os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ౴")] = json.dumps(CONFIG)
  os.environ[bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ౵")] = bstack1lll11l111_opy_
  os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭౶")] = str(bstack11l11l1l_opy_)
  os.environ[bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ౷")] = str(True)
  if bstack1l11l111l_opy_(arg, [bstack111l1ll_opy_ (u"ࠧ࠮ࡰࠪ౸"), bstack111l1ll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ౹")]) != -1:
    os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ౺")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll11111l_opy_)
    return
  bstack1l11ll1ll1_opy_()
  global bstack1ll11lll1l_opy_
  global bstack1ll11l11l_opy_
  global bstack1l1ll1l11l_opy_
  global bstack1ll111l1ll_opy_
  global bstack1ll1llll_opy_
  global bstack1llll111l1_opy_
  global bstack111lll1ll_opy_
  arg.append(bstack111l1ll_opy_ (u"ࠥ࠱࡜ࠨ౻"))
  arg.append(bstack111l1ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ౼"))
  arg.append(bstack111l1ll_opy_ (u"ࠧ࠳ࡗࠣ౽"))
  arg.append(bstack111l1ll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ౾"))
  global bstack1ll111ll_opy_
  global bstack1lllll11ll_opy_
  global bstack1ll1l1ll_opy_
  global bstack11ll1lll1_opy_
  global bstack1l111l11ll_opy_
  global bstack11llll1l1_opy_
  global bstack1l1ll1111_opy_
  global bstack1l11111111_opy_
  global bstack1l11ll11l_opy_
  global bstack1l1llllll_opy_
  global bstack1ll11l111_opy_
  global bstack1llll11ll_opy_
  global bstack1llll1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll111ll_opy_ = webdriver.Remote.__init__
    bstack1lllll11ll_opy_ = WebDriver.quit
    bstack1l11111111_opy_ = WebDriver.close
    bstack1l11ll11l_opy_ = WebDriver.get
    bstack1ll1l1ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lll1ll1l1_opy_(CONFIG) and bstack1l11ll1l_opy_():
    if bstack1llll11lll_opy_() < version.parse(bstack11lllll1ll_opy_):
      logger.error(bstack1ll11111l_opy_.format(bstack1llll11lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1llllll_opy_ = RemoteConnection._1l1111lll_opy_
      except Exception as e:
        logger.error(bstack1l11lll1ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll11l111_opy_ = Config.getoption
    from _pytest import runner
    bstack1llll11ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l1ll1ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1llll1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l1ll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ౿"))
  bstack1l1ll1l11l_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಀ"), {}).get(bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಁ"))
  bstack111lll1ll_opy_ = True
  bstack1l1ll1ll1l_opy_(bstack1l1lll1l1_opy_)
  os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫಂ")] = CONFIG[bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ಃ")]
  os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ಄")] = CONFIG[bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಅ")]
  os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪಆ")] = bstack1ll1ll11l_opy_.__str__()
  from _pytest.config import main as bstack1l11l1l1l1_opy_
  bstack11l1lll1l_opy_ = []
  try:
    bstack1l11l1lll_opy_ = bstack1l11l1l1l1_opy_(arg)
    if bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬಇ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l111l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1lll1l_opy_.append(bstack11l111l11_opy_)
    try:
      bstack11ll11111_opy_ = (bstack11l1lll1l_opy_, int(bstack1l11l1lll_opy_))
      bstack1l1lll1ll1_opy_.append(bstack11ll11111_opy_)
    except:
      bstack1l1lll1ll1_opy_.append((bstack11l1lll1l_opy_, bstack1l11l1lll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11l1lll1l_opy_.append({bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಈ"): bstack111l1ll_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬಉ") + os.environ.get(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫಊ")), bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫಋ"): traceback.format_exc(), bstack111l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬಌ"): int(os.environ.get(bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ಍")))})
    bstack1l1lll1ll1_opy_.append((bstack11l1lll1l_opy_, 1))
def bstack111ll1111_opy_(arg):
  global bstack1l1l1l111_opy_
  bstack1l1ll1ll1l_opy_(bstack1l11l11l1_opy_)
  os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಎ")] = str(bstack11l11l1l_opy_)
  from behave.__main__ import main as bstack1llll1l1ll_opy_
  status_code = bstack1llll1l1ll_opy_(arg)
  if status_code != 0:
    bstack1l1l1l111_opy_ = status_code
def bstack111ll111l_opy_():
  logger.info(bstack1ll111ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨಏ"), help=bstack111l1ll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫಐ"))
  parser.add_argument(bstack111l1ll_opy_ (u"ࠫ࠲ࡻࠧ಑"), bstack111l1ll_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩಒ"), help=bstack111l1ll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬಓ"))
  parser.add_argument(bstack111l1ll_opy_ (u"ࠧ࠮࡭ࠪಔ"), bstack111l1ll_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧಕ"), help=bstack111l1ll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪಖ"))
  parser.add_argument(bstack111l1ll_opy_ (u"ࠪ࠱࡫࠭ಗ"), bstack111l1ll_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಘ"), help=bstack111l1ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫಙ"))
  bstack1ll11ll11l_opy_ = parser.parse_args()
  try:
    bstack1lll11lll_opy_ = bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪಚ")
    if bstack1ll11ll11l_opy_.framework and bstack1ll11ll11l_opy_.framework not in (bstack111l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧಛ"), bstack111l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩಜ")):
      bstack1lll11lll_opy_ = bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨಝ")
    bstack11ll1l1l1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11lll_opy_)
    bstack1l1l1lll_opy_ = open(bstack11ll1l1l1l_opy_, bstack111l1ll_opy_ (u"ࠪࡶࠬಞ"))
    bstack11ll11l11_opy_ = bstack1l1l1lll_opy_.read()
    bstack1l1l1lll_opy_.close()
    if bstack1ll11ll11l_opy_.username:
      bstack11ll11l11_opy_ = bstack11ll11l11_opy_.replace(bstack111l1ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫಟ"), bstack1ll11ll11l_opy_.username)
    if bstack1ll11ll11l_opy_.key:
      bstack11ll11l11_opy_ = bstack11ll11l11_opy_.replace(bstack111l1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧಠ"), bstack1ll11ll11l_opy_.key)
    if bstack1ll11ll11l_opy_.framework:
      bstack11ll11l11_opy_ = bstack11ll11l11_opy_.replace(bstack111l1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧಡ"), bstack1ll11ll11l_opy_.framework)
    file_name = bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪಢ")
    file_path = os.path.abspath(file_name)
    bstack1lll1lll1_opy_ = open(file_path, bstack111l1ll_opy_ (u"ࠨࡹࠪಣ"))
    bstack1lll1lll1_opy_.write(bstack11ll11l11_opy_)
    bstack1lll1lll1_opy_.close()
    logger.info(bstack11lll11l1_opy_)
    try:
      os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫತ")] = bstack1ll11ll11l_opy_.framework if bstack1ll11ll11l_opy_.framework != None else bstack111l1ll_opy_ (u"ࠥࠦಥ")
      config = yaml.safe_load(bstack11ll11l11_opy_)
      config[bstack111l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫದ")] = bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫಧ")
      bstack11l1l1ll1_opy_(bstack1l1l111l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l1l11ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll11ll1_opy_.format(str(e)))
def bstack11l1l1ll1_opy_(bstack1l11111lll_opy_, config, bstack1l1l1111ll_opy_={}):
  global bstack1ll1ll11l_opy_
  global bstack1l1ll1111l_opy_
  global bstack1ll11lll_opy_
  if not config:
    return
  bstack1llll1ll11_opy_ = bstack1ll111l11l_opy_ if not bstack1ll1ll11l_opy_ else (
    bstack111l1lll_opy_ if bstack111l1ll_opy_ (u"࠭ࡡࡱࡲࠪನ") in config else (
        bstack1llll1lll1_opy_ if config.get(bstack111l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ಩")) else bstack11ll111l_opy_
    )
)
  bstack1l1llll1l1_opy_ = False
  bstack1ll111l111_opy_ = False
  if bstack1ll1ll11l_opy_ is True:
      if bstack111l1ll_opy_ (u"ࠨࡣࡳࡴࠬಪ") in config:
          bstack1l1llll1l1_opy_ = True
      else:
          bstack1ll111l111_opy_ = True
  bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l111l1ll_opy_(config, bstack1l1ll1111l_opy_)
  bstack1llll1111_opy_ = bstack1l1ll11111_opy_()
  data = {
    bstack111l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಫ"): config[bstack111l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬಬ")],
    bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧಭ"): config[bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨಮ")],
    bstack111l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪಯ"): bstack1l11111lll_opy_,
    bstack111l1ll_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫರ"): os.environ.get(bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಱ"), bstack1l1ll1111l_opy_),
    bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫಲ"): bstack1ll11l11_opy_,
    bstack111l1ll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬಳ"): bstack11ll1ll1l1_opy_(),
    bstack111l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ಴"): {
      bstack111l1ll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪವ"): str(config[bstack111l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ಶ")]) if bstack111l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧಷ") in config else bstack111l1ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤಸ"),
      bstack111l1ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫಹ"): sys.version,
      bstack111l1ll_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ಺"): bstack11ll111111_opy_(os.environ.get(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭಻"), bstack1l1ll1111l_opy_)),
      bstack111l1ll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫಼ࠧ"): bstack111l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಽ"),
      bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨಾ"): bstack1llll1ll11_opy_,
      bstack111l1ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ಿ"): bstack1l11ll1ll_opy_,
      bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨೀ"): os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨು")],
      bstack111l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೂ"): os.environ.get(bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧೃ"), bstack1l1ll1111l_opy_),
      bstack111l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩೄ"): bstack1lllllll1_opy_(os.environ.get(bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೅"), bstack1l1ll1111l_opy_)),
      bstack111l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೆ"): bstack1llll1111_opy_.get(bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೇ")),
      bstack111l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩೈ"): bstack1llll1111_opy_.get(bstack111l1ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೉")),
      bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨೊ"): config[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩೋ")] if config[bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪೌ")] else bstack111l1ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ್"),
      bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೎"): str(config[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೏")]) if bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೐") in config else bstack111l1ll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ೑"),
      bstack111l1ll_opy_ (u"࠭࡯ࡴࠩ೒"): sys.platform,
      bstack111l1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ೓"): socket.gethostname(),
      bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ೔"): bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫೕ"))
    }
  }
  if not bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪೖ")) is None:
    data[bstack111l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೗")][bstack111l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ೘")] = {
      bstack111l1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭೙"): bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ೚"),
      bstack111l1ll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ೛"): bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ೜")),
      bstack111l1ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩೝ"): bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧೞ"))
    }
  if bstack1l11111lll_opy_ == bstack1l111l1l_opy_:
    data[bstack111l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೟")][bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫೠ")] = bstack1l1ll1l111_opy_(config)
    data[bstack111l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪೡ")][bstack111l1ll_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ೢ")] = percy.bstack1ll1ll1l_opy_
    data[bstack111l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬೣ")][bstack111l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩ೤")] = percy.bstack1l1ll11lll_opy_
  update(data[bstack111l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೥")], bstack1l1l1111ll_opy_)
  try:
    response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠬࡖࡏࡔࡖࠪ೦"), bstack1lll111l11_opy_(bstack1l1lll111_opy_), data, {
      bstack111l1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ೧"): (config[bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೨")], config[bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೩")])
    })
    if response:
      logger.debug(bstack1lll1l1l1l_opy_.format(bstack1l11111lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l111111l1_opy_.format(str(e)))
def bstack11ll111111_opy_(framework):
  return bstack111l1ll_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ೪").format(str(framework), __version__) if framework else bstack111l1ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ೫").format(
    __version__)
def bstack1l11ll1ll1_opy_():
  global CONFIG
  global bstack1l111ll111_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll11l11ll_opy_()
    logger.debug(bstack1l1l1l1ll1_opy_.format(str(CONFIG)))
    bstack1l111ll111_opy_ = bstack1111ll11_opy_.bstack1l1l11l11l_opy_(CONFIG, bstack1l111ll111_opy_)
    bstack11ll1l1ll1_opy_()
  except Exception as e:
    logger.error(bstack111l1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣ೬") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111ll1_opy_
  atexit.register(bstack1111ll1ll_opy_)
  signal.signal(signal.SIGINT, bstack111ll111_opy_)
  signal.signal(signal.SIGTERM, bstack111ll111_opy_)
def bstack1ll111ll1_opy_(exctype, value, traceback):
  global bstack1ll1ll11ll_opy_
  try:
    for driver in bstack1ll1ll11ll_opy_:
      bstack11l1lllll1_opy_(driver, bstack111l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೭"), bstack111l1ll_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ೮") + str(value))
  except Exception:
    pass
  bstack1111l1ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1111l1ll1_opy_(message=bstack111l1ll_opy_ (u"ࠧࠨ೯"), bstack1l11llll11_opy_ = False):
  global CONFIG
  bstack11llllll_opy_ = bstack111l1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪ೰") if bstack1l11llll11_opy_ else bstack111l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨೱ")
  try:
    if message:
      bstack1l1l1111ll_opy_ = {
        bstack11llllll_opy_ : str(message)
      }
      bstack11l1l1ll1_opy_(bstack1l111l1l_opy_, CONFIG, bstack1l1l1111ll_opy_)
    else:
      bstack11l1l1ll1_opy_(bstack1l111l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(str(e)))
def bstack11lll11l11_opy_(bstack1lllll1l1l_opy_, size):
  bstack11l1l11ll_opy_ = []
  while len(bstack1lllll1l1l_opy_) > size:
    bstack111l11lll_opy_ = bstack1lllll1l1l_opy_[:size]
    bstack11l1l11ll_opy_.append(bstack111l11lll_opy_)
    bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_[size:]
  bstack11l1l11ll_opy_.append(bstack1lllll1l1l_opy_)
  return bstack11l1l11ll_opy_
def bstack1l11l111ll_opy_(args):
  if bstack111l1ll_opy_ (u"ࠪ࠱ࡲ࠭ೲ") in args and bstack111l1ll_opy_ (u"ࠫࡵࡪࡢࠨೳ") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1l1l11_opy_=None, bstack1l1lll1ll1_opy_=None, bstack11111l11l_opy_=False):
  global CONFIG
  global bstack1lll11l111_opy_
  global bstack11l11l1l_opy_
  global bstack1l1ll1111l_opy_
  global bstack1ll11lll_opy_
  bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠬ࠭೴")
  bstack1l11ll11_opy_(bstack11l1llll_opy_, logger)
  if bstack1ll1l1l11_opy_ and isinstance(bstack1ll1l1l11_opy_, str):
    bstack1ll1l1l11_opy_ = eval(bstack1ll1l1l11_opy_)
  if bstack1ll1l1l11_opy_:
    CONFIG = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭೵")]
    bstack1lll11l111_opy_ = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೶")]
    bstack11l11l1l_opy_ = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೷")]
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ೸"), bstack11l11l1l_opy_)
    bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ೹")
  bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭೺"), uuid4().__str__())
  logger.info(bstack111l1ll_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ೻") + bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ೼")));
  logger.debug(bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪ೽") + bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ೾")))
  if not bstack11111l11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll11111l_opy_)
      return
    if sys.argv[1] == bstack111l1ll_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೿") or sys.argv[1] == bstack111l1ll_opy_ (u"ࠪ࠱ࡻ࠭ഀ"):
      logger.info(bstack111l1ll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫഁ").format(__version__))
      return
    if sys.argv[1] == bstack111l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫം"):
      bstack111ll111l_opy_()
      return
  args = sys.argv
  bstack1l11ll1ll1_opy_()
  global bstack1ll11lll1l_opy_
  global bstack1lll1l1ll_opy_
  global bstack111lll1ll_opy_
  global bstack1ll11l1l11_opy_
  global bstack1ll11l11l_opy_
  global bstack1l1ll1l11l_opy_
  global bstack1ll111l1ll_opy_
  global bstack11lll11l_opy_
  global bstack1ll1llll_opy_
  global bstack1llll111l1_opy_
  global bstack1l1111l1ll_opy_
  bstack1lll1l1ll_opy_ = len(CONFIG.get(bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഃ"), []))
  if not bstack11lll1lll_opy_:
    if args[1] == bstack111l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഄ") or args[1] == bstack111l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩഅ"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩആ")
      args = args[2:]
    elif args[1] == bstack111l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩഇ"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഈ")
      args = args[2:]
    elif args[1] == bstack111l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫഉ"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬഊ")
      args = args[2:]
    elif args[1] == bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨഋ"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩഌ")
      args = args[2:]
    elif args[1] == bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ഍"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪഎ")
      args = args[2:]
    elif args[1] == bstack111l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഏ"):
      bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬഐ")
      args = args[2:]
    else:
      if not bstack111l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ഑") in CONFIG or str(CONFIG[bstack111l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪഒ")]).lower() in [bstack111l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഓ"), bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪഔ")]:
        bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪക")
        args = args[1:]
      elif str(CONFIG[bstack111l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഖ")]).lower() == bstack111l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഗ"):
        bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬഘ")
        args = args[1:]
      elif str(CONFIG[bstack111l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪങ")]).lower() == bstack111l1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧച"):
        bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨഛ")
        args = args[1:]
      elif str(CONFIG[bstack111l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ജ")]).lower() == bstack111l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫഝ"):
        bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഞ")
        args = args[1:]
      elif str(CONFIG[bstack111l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩട")]).lower() == bstack111l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧഠ"):
        bstack11lll1lll_opy_ = bstack111l1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഡ")
        args = args[1:]
      else:
        os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഢ")] = bstack11lll1lll_opy_
        bstack1ll1l111ll_opy_(bstack1lll111l1l_opy_)
  os.environ[bstack111l1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫണ")] = bstack11lll1lll_opy_
  bstack1l1ll1111l_opy_ = bstack11lll1lll_opy_
  global bstack1l1l1lll1_opy_
  global bstack111lllll_opy_
  if bstack1ll1l1l11_opy_:
    try:
      os.environ[bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ത")] = bstack11lll1lll_opy_
      bstack11l1l1ll1_opy_(bstack1ll11l1ll1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l11111l_opy_.format(str(e)))
  global bstack1ll111ll_opy_
  global bstack1lllll11ll_opy_
  global bstack11l1l11l1_opy_
  global bstack1l1111ll_opy_
  global bstack1lll1l111_opy_
  global bstack1l11ll1l1_opy_
  global bstack11ll1lll1_opy_
  global bstack1l111l11ll_opy_
  global bstack1l1ll1ll1_opy_
  global bstack11llll1l1_opy_
  global bstack1l1ll1111_opy_
  global bstack1l11111111_opy_
  global bstack1l11l111l1_opy_
  global bstack1l11111ll1_opy_
  global bstack1l11ll11l_opy_
  global bstack1l1llllll_opy_
  global bstack1ll11l111_opy_
  global bstack1llll11ll_opy_
  global bstack111l11l11_opy_
  global bstack1llll1ll_opy_
  global bstack1ll1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll111ll_opy_ = webdriver.Remote.__init__
    bstack1lllll11ll_opy_ = WebDriver.quit
    bstack1l11111111_opy_ = WebDriver.close
    bstack1l11ll11l_opy_ = WebDriver.get
    bstack1ll1l1ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l1lll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1l1111_opy_
    bstack111lllll_opy_ = bstack1ll1l1111_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lll1l11l_opy_
    from QWeb.keywords import browser
    bstack1lll1l11l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll1ll1l1_opy_(CONFIG) and bstack1l11ll1l_opy_():
    if bstack1llll11lll_opy_() < version.parse(bstack11lllll1ll_opy_):
      logger.error(bstack1ll11111l_opy_.format(bstack1llll11lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1llllll_opy_ = RemoteConnection._1l1111lll_opy_
      except Exception as e:
        logger.error(bstack1l11lll1ll_opy_.format(str(e)))
  if not CONFIG.get(bstack111l1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧഥ"), False) and not bstack1ll1l1l11_opy_:
    logger.info(bstack1l11ll1111_opy_)
  if bstack111l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪദ") in CONFIG and str(CONFIG[bstack111l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫധ")]).lower() != bstack111l1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧന"):
    bstack1llll1l1l_opy_()
  elif bstack11lll1lll_opy_ != bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഩ") or (bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪപ") and not bstack1ll1l1l11_opy_):
    bstack11lll1ll11_opy_()
  if (bstack11lll1lll_opy_ in [bstack111l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪഫ"), bstack111l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫബ"), bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഭ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11ll11ll1l_opy_
        bstack1l11ll1l1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1lllll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1l111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l1l11l_opy_ + str(e))
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll1_opy_)
    if bstack11lll1lll_opy_ != bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨമ"):
      bstack1l1l1l1l1l_opy_()
    bstack11l1l11l1_opy_ = Output.start_test
    bstack1l1111ll_opy_ = Output.end_test
    bstack11ll1lll1_opy_ = TestStatus.__init__
    bstack1l1ll1ll1_opy_ = pabot._run
    bstack11llll1l1_opy_ = QueueItem.__init__
    bstack1l1ll1111_opy_ = pabot._create_command_for_execution
    bstack111l11l11_opy_ = pabot._report_results
  if bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨയ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll_opy_)
    bstack1l11l111l1_opy_ = Runner.run_hook
    bstack1l11111ll1_opy_ = Step.run
  if bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩര"):
    try:
      from _pytest.config import Config
      bstack1ll11l111_opy_ = Config.getoption
      from _pytest import runner
      bstack1llll11ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1ll1ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1llll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫറ"))
  try:
    framework_name = bstack111l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪല") if bstack11lll1lll_opy_ in [bstack111l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫള"), bstack111l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬഴ"), bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨവ")] else bstack1l1l11l1l1_opy_(bstack11lll1lll_opy_)
    bstack1llll1ll1_opy_ = {
      bstack111l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩശ"): bstack111l1ll_opy_ (u"ࠩࡾ࠴ࢂ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨഷ").format(framework_name) if bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪസ") and bstack1l11l11ll1_opy_() else framework_name,
      bstack111l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨഹ"): bstack1lllllll1_opy_(framework_name),
      bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪഺ"): __version__,
      bstack111l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪ഻ࠧ"): bstack11lll1lll_opy_
    }
    if bstack11lll1lll_opy_ in bstack111l1l111_opy_:
      if bstack1ll1ll11l_opy_ and bstack111l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ഼ࠧ") in CONFIG and CONFIG[bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨഽ")] == True:
        if bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩാ") in CONFIG:
          os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫി")] = os.getenv(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬീ"), json.dumps(CONFIG[bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬു")]))
          CONFIG[bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ൂ")].pop(bstack111l1ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬൃ"), None)
          CONFIG[bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨൄ")].pop(bstack111l1ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ൅"), None)
        bstack1llll1ll1_opy_[bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪെ")] = {
          bstack111l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩേ"): bstack111l1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧൈ"),
          bstack111l1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ൉"): str(bstack1llll11lll_opy_())
        }
    if bstack11lll1lll_opy_ not in [bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨൊ")]:
      bstack1lllll11l_opy_ = bstack1lll1ll111_opy_.launch(CONFIG, bstack1llll1ll1_opy_)
  except Exception as e:
    logger.debug(bstack1l111111ll_opy_.format(bstack111l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩോ"), str(e)))
  if bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩൌ"):
    bstack111lll1ll_opy_ = True
    if bstack1ll1l1l11_opy_ and bstack11111l11l_opy_:
      bstack1l1ll1l11l_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ്ࠧ"), {}).get(bstack111l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ൎ"))
      bstack1l1ll1ll1l_opy_(bstack1l1lllll_opy_)
    elif bstack1ll1l1l11_opy_:
      bstack1l1ll1l11l_opy_ = CONFIG.get(bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൏"), {}).get(bstack111l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ൐"))
      global bstack1ll1ll11ll_opy_
      try:
        if bstack1l11l111ll_opy_(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൑")]) and multiprocessing.current_process().name == bstack111l1ll_opy_ (u"ࠨ࠲ࠪ൒"):
          bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൓")].remove(bstack111l1ll_opy_ (u"ࠪ࠱ࡲ࠭ൔ"))
          bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൕ")].remove(bstack111l1ll_opy_ (u"ࠬࡶࡤࡣࠩൖ"))
          bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൗ")] = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൘")][0]
          with open(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൙")], bstack111l1ll_opy_ (u"ࠩࡵࠫ൚")) as f:
            bstack1l111lll1l_opy_ = f.read()
          bstack1l11lll1l_opy_ = bstack111l1ll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ൛").format(str(bstack1ll1l1l11_opy_))
          bstack1ll1lll1ll_opy_ = bstack1l11lll1l_opy_ + bstack1l111lll1l_opy_
          bstack1l11lll11_opy_ = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ൜")] + bstack111l1ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ൝")
          with open(bstack1l11lll11_opy_, bstack111l1ll_opy_ (u"࠭ࡷࠨ൞")):
            pass
          with open(bstack1l11lll11_opy_, bstack111l1ll_opy_ (u"ࠢࡸ࠭ࠥൟ")) as f:
            f.write(bstack1ll1lll1ll_opy_)
          import subprocess
          bstack111lll11_opy_ = subprocess.run([bstack111l1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣൠ"), bstack1l11lll11_opy_])
          if os.path.exists(bstack1l11lll11_opy_):
            os.unlink(bstack1l11lll11_opy_)
          os._exit(bstack111lll11_opy_.returncode)
        else:
          if bstack1l11l111ll_opy_(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬൡ")]):
            bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ൢ")].remove(bstack111l1ll_opy_ (u"ࠫ࠲ࡳࠧൣ"))
            bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൤")].remove(bstack111l1ll_opy_ (u"࠭ࡰࡥࡤࠪ൥"))
            bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൦")] = bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൧")][0]
          bstack1l1ll1ll1l_opy_(bstack1l1lllll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൨")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l1ll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ൩")] = bstack111l1ll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭൪")
          mod_globals[bstack111l1ll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ൫")] = os.path.abspath(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ൬")])
          exec(open(bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൭")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l1ll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ൮").format(str(e)))
          for driver in bstack1ll1ll11ll_opy_:
            bstack1l1lll1ll1_opy_.append({
              bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ൯"): bstack1ll1l1l11_opy_[bstack111l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൰")],
              bstack111l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ൱"): str(e),
              bstack111l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ൲"): multiprocessing.current_process().name
            })
            bstack11l1lllll1_opy_(driver, bstack111l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭൳"), bstack111l1ll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ൴") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1ll11ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l11l1l_opy_, CONFIG, logger)
      bstack1llllll1ll_opy_()
      bstack11ll11l1ll_opy_()
      bstack11ll11l1l1_opy_ = {
        bstack111l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൵"): args[0],
        bstack111l1ll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ൶"): CONFIG,
        bstack111l1ll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ൷"): bstack1lll11l111_opy_,
        bstack111l1ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭൸"): bstack11l11l1l_opy_
      }
      percy.bstack1ll1lll11l_opy_()
      if bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൹") in CONFIG:
        bstack1l11l11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l11l1l1l_opy_ = manager.list()
        if bstack1l11l111ll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩൺ")]):
            if index == 0:
              bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൻ")] = args
            bstack1l11l11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11ll11l1l1_opy_, bstack1l11l1l1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫർ")]):
            bstack1l11l11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11ll11l1l1_opy_, bstack1l11l1l1l_opy_)))
        for t in bstack1l11l11l11_opy_:
          t.start()
        for t in bstack1l11l11l11_opy_:
          t.join()
        bstack11lll11l_opy_ = list(bstack1l11l1l1l_opy_)
      else:
        if bstack1l11l111ll_opy_(args):
          bstack11ll11l1l1_opy_[bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬൽ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11ll11l1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1ll1ll1l_opy_(bstack1l1lllll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l1ll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬൾ")] = bstack111l1ll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ൿ")
          mod_globals[bstack111l1ll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ඀")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඁ") or bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ං"):
    percy.init(bstack11l11l1l_opy_, CONFIG, logger)
    percy.bstack1ll1lll11l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll1_opy_)
    bstack1llllll1ll_opy_()
    bstack1l1ll1ll1l_opy_(bstack1ll111l1_opy_)
    if bstack1ll1ll11l_opy_:
      bstack1l1lllllll_opy_(bstack1ll111l1_opy_, args)
      if bstack111l1ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඃ") in args:
        i = args.index(bstack111l1ll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ඄"))
        args.pop(i)
        args.pop(i)
      if bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭අ") not in CONFIG:
        CONFIG[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧආ")] = [{}]
        bstack1lll1l1ll_opy_ = 1
      if bstack1ll11lll1l_opy_ == 0:
        bstack1ll11lll1l_opy_ = 1
      args.insert(0, str(bstack1ll11lll1l_opy_))
      args.insert(0, str(bstack111l1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඇ")))
    if bstack1lll1ll111_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll111l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1111ll11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l1ll_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨඈ"),
        ).parse_args(bstack1ll111l11_opy_)
        bstack11lll111_opy_ = args.index(bstack1ll111l11_opy_[0]) if len(bstack1ll111l11_opy_) > 0 else len(args)
        args.insert(bstack11lll111_opy_, str(bstack111l1ll_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫඉ")))
        args.insert(bstack11lll111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬඊ"))))
        if bstack1l1111111_opy_(os.environ.get(bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧඋ"))) and str(os.environ.get(bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧඌ"), bstack111l1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩඍ"))) != bstack111l1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪඎ"):
          for bstack111lll11l_opy_ in bstack1l1111ll11_opy_:
            args.remove(bstack111lll11l_opy_)
          bstack11l11lll1_opy_ = os.environ.get(bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪඏ")).split(bstack111l1ll_opy_ (u"ࠧ࠭ࠩඐ"))
          for bstack1lll1ll1l_opy_ in bstack11l11lll1_opy_:
            args.append(bstack1lll1ll1l_opy_)
      except Exception as e:
        logger.error(bstack111l1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࠦඑ").format(e))
    pabot.main(args)
  elif bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪඒ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll1_opy_)
    for a in args:
      if bstack111l1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩඓ") in a:
        bstack1ll11l11l_opy_ = int(a.split(bstack111l1ll_opy_ (u"ࠫ࠿࠭ඔ"))[1])
      if bstack111l1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩඕ") in a:
        bstack1l1ll1l11l_opy_ = str(a.split(bstack111l1ll_opy_ (u"࠭࠺ࠨඖ"))[1])
      if bstack111l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ඗") in a:
        bstack1ll111l1ll_opy_ = str(a.split(bstack111l1ll_opy_ (u"ࠨ࠼ࠪ඘"))[1])
    bstack1ll1l11ll_opy_ = None
    if bstack111l1ll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ඙") in args:
      i = args.index(bstack111l1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩක"))
      args.pop(i)
      bstack1ll1l11ll_opy_ = args.pop(i)
    if bstack1ll1l11ll_opy_ is not None:
      global bstack1lll1111l_opy_
      bstack1lll1111l_opy_ = bstack1ll1l11ll_opy_
    bstack1l1ll1ll1l_opy_(bstack1ll111l1_opy_)
    run_cli(args)
    if bstack111l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨඛ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l111l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1lll1ll1_opy_.append(bstack11l111l11_opy_)
  elif bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬග"):
    percy.init(bstack11l11l1l_opy_, CONFIG, logger)
    percy.bstack1ll1lll11l_opy_()
    bstack11l1lll1_opy_ = bstack1l1l11ll1l_opy_(args, logger, CONFIG, bstack1ll1ll11l_opy_)
    bstack11l1lll1_opy_.bstack1l11lll1l1_opy_()
    bstack1llllll1ll_opy_()
    bstack1ll11l1l11_opy_ = True
    bstack1llll111l1_opy_ = bstack11l1lll1_opy_.bstack1l1llll1_opy_()
    bstack11l1lll1_opy_.bstack11ll11l1l1_opy_(bstack1ll11l1l1l_opy_)
    bstack1l1llll1l_opy_ = bstack11l1lll1_opy_.bstack1ll11l1l1_opy_(bstack11111ll1_opy_, {
      bstack111l1ll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧඝ"): bstack1lll11l111_opy_,
      bstack111l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩඞ"): bstack11l11l1l_opy_,
      bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫඟ"): bstack1ll1ll11l_opy_
    })
    try:
      bstack11l1lll1l_opy_, bstack1ll11ll11_opy_ = map(list, zip(*bstack1l1llll1l_opy_))
      bstack1ll1llll_opy_ = bstack11l1lll1l_opy_[0]
      for status_code in bstack1ll11ll11_opy_:
        if status_code != 0:
          bstack1l1111l1ll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢච").format(str(e)))
  elif bstack11lll1lll_opy_ == bstack111l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪඡ"):
    try:
      from behave.__main__ import main as bstack1llll1l1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll11ll_opy_(e, bstack1ll1lllll_opy_)
    bstack1llllll1ll_opy_()
    bstack1ll11l1l11_opy_ = True
    bstack1l111lllll_opy_ = 1
    if bstack111l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫජ") in CONFIG:
      bstack1l111lllll_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬඣ")]
    if bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඤ") in CONFIG:
      bstack1l1l11l11_opy_ = int(bstack1l111lllll_opy_) * int(len(CONFIG[bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඥ")]))
    else:
      bstack1l1l11l11_opy_ = int(bstack1l111lllll_opy_)
    config = Configuration(args)
    bstack1ll1ll1lll_opy_ = config.paths
    if len(bstack1ll1ll1lll_opy_) == 0:
      import glob
      pattern = bstack111l1ll_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧඦ")
      bstack1l1l1llll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1l1llll1_opy_)
      config = Configuration(args)
      bstack1ll1ll1lll_opy_ = config.paths
    bstack11ll1lll1l_opy_ = [os.path.normpath(item) for item in bstack1ll1ll1lll_opy_]
    bstack1llll1l111_opy_ = [os.path.normpath(item) for item in args]
    bstack111l1l1ll_opy_ = [item for item in bstack1llll1l111_opy_ if item not in bstack11ll1lll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l1ll_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪට"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1lll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll1l1ll1_opy_)))
                    for bstack1lll1l1ll1_opy_ in bstack11ll1lll1l_opy_]
    bstack1l111l11l1_opy_ = []
    for spec in bstack11ll1lll1l_opy_:
      bstack1ll111llll_opy_ = []
      bstack1ll111llll_opy_ += bstack111l1l1ll_opy_
      bstack1ll111llll_opy_.append(spec)
      bstack1l111l11l1_opy_.append(bstack1ll111llll_opy_)
    execution_items = []
    for bstack1ll111llll_opy_ in bstack1l111l11l1_opy_:
      if bstack111l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ඨ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඩ")]):
          item = {}
          item[bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࠩඪ")] = bstack111l1ll_opy_ (u"࠭ࠠࠨණ").join(bstack1ll111llll_opy_)
          item[bstack111l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ඬ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111l1ll_opy_ (u"ࠨࡣࡵ࡫ࠬත")] = bstack111l1ll_opy_ (u"ࠩࠣࠫථ").join(bstack1ll111llll_opy_)
        item[bstack111l1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩද")] = 0
        execution_items.append(item)
    bstack1111ll111_opy_ = bstack11lll11l11_opy_(execution_items, bstack1l1l11l11_opy_)
    for execution_item in bstack1111ll111_opy_:
      bstack1l11l11l11_opy_ = []
      for item in execution_item:
        bstack1l11l11l11_opy_.append(bstack1ll1ll1ll_opy_(name=str(item[bstack111l1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪධ")]),
                                             target=bstack111ll1111_opy_,
                                             args=(item[bstack111l1ll_opy_ (u"ࠬࡧࡲࡨࠩන")],)))
      for t in bstack1l11l11l11_opy_:
        t.start()
      for t in bstack1l11l11l11_opy_:
        t.join()
  else:
    bstack1ll1l111ll_opy_(bstack1lll111l1l_opy_)
  if not bstack1ll1l1l11_opy_:
    bstack11111lll_opy_()
    if(bstack11lll1lll_opy_ in [bstack111l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭඲"), bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧඳ")]):
      bstack1l1l11l1ll_opy_()
  bstack1111ll11_opy_.bstack1111lll1_opy_()
def browserstack_initialize(bstack11ll11ll11_opy_=None):
  logger.info(bstack111l1ll_opy_ (u"ࠨࡔࡸࡲࡳ࡯࡮ࡨࠢࡖࡈࡐࠦࡷࡪࡶ࡫ࠤࡦࡸࡧࡴ࠼ࠣࠫප") + str(bstack11ll11ll11_opy_))
  run_on_browserstack(bstack11ll11ll11_opy_, None, True)
@measure(event_name=EVENTS.bstack1l1l1l1l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack11111lll_opy_():
  global CONFIG
  global bstack1l1ll1111l_opy_
  global bstack1l1111l1ll_opy_
  global bstack1l1l1l111_opy_
  global bstack1ll11lll_opy_
  bstack1lll1ll111_opy_.stop()
  bstack11l111ll1_opy_.bstack1l11ll11ll_opy_()
  if bstack111l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ඵ") in CONFIG and str(CONFIG[bstack111l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧබ")]).lower() != bstack111l1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪභ"):
    bstack11ll1ll1_opy_, bstack111ll1l11_opy_ = bstack1l1lll1l11_opy_()
  else:
    bstack11ll1ll1_opy_, bstack111ll1l11_opy_ = get_build_link()
  bstack1ll1111lll_opy_(bstack11ll1ll1_opy_)
  logger.info(bstack111l1ll_opy_ (u"࡙ࠬࡄࡌࠢࡵࡹࡳࠦࡥ࡯ࡦࡨࡨࠥ࡬࡯ࡳࠢ࡬ࡨ࠿࠭ම") + bstack1ll11lll_opy_.get_property(bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨඹ"), bstack111l1ll_opy_ (u"ࠧࠨය")) + bstack111l1ll_opy_ (u"ࠨ࠮ࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡮ࡪ࠺ࠡࠩර") + os.getenv(bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ඼"), bstack111l1ll_opy_ (u"ࠪࠫල")))
  if bstack11ll1ll1_opy_ is not None and bstack11llll1111_opy_() != -1:
    sessions = bstack1l1111lll1_opy_(bstack11ll1ll1_opy_)
    bstack1111l111l_opy_(sessions, bstack111ll1l11_opy_)
  if bstack1l1ll1111l_opy_ == bstack111l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ඾") and bstack1l1111l1ll_opy_ != 0:
    sys.exit(bstack1l1111l1ll_opy_)
  if bstack1l1ll1111l_opy_ == bstack111l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ඿") and bstack1l1l1l111_opy_ != 0:
    sys.exit(bstack1l1l1l111_opy_)
def bstack1ll1111lll_opy_(new_id):
    global bstack1ll11l11_opy_
    bstack1ll11l11_opy_ = new_id
def bstack1l1l11l1l1_opy_(bstack1ll11llll1_opy_):
  if bstack1ll11llll1_opy_:
    return bstack1ll11llll1_opy_.capitalize()
  else:
    return bstack111l1ll_opy_ (u"࠭ࠧව")
@measure(event_name=EVENTS.bstack1ll11111l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1llllllll1_opy_(bstack11l1lll11_opy_):
  if bstack111l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬශ") in bstack11l1lll11_opy_ and bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ෂ")] != bstack111l1ll_opy_ (u"ࠩࠪස"):
    return bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨහ")]
  else:
    bstack11l1111ll_opy_ = bstack111l1ll_opy_ (u"ࠦࠧළ")
    if bstack111l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬෆ") in bstack11l1lll11_opy_ and bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෇")] != None:
      bstack11l1111ll_opy_ += bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ෈")] + bstack111l1ll_opy_ (u"ࠣ࠮ࠣࠦ෉")
      if bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠩࡲࡷ්ࠬ")] == bstack111l1ll_opy_ (u"ࠥ࡭ࡴࡹࠢ෋"):
        bstack11l1111ll_opy_ += bstack111l1ll_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ෌")
      bstack11l1111ll_opy_ += (bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෍")] or bstack111l1ll_opy_ (u"࠭ࠧ෎"))
      return bstack11l1111ll_opy_
    else:
      bstack11l1111ll_opy_ += bstack1l1l11l1l1_opy_(bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨා")]) + bstack111l1ll_opy_ (u"ࠣࠢࠥැ") + (
              bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫෑ")] or bstack111l1ll_opy_ (u"ࠪࠫි")) + bstack111l1ll_opy_ (u"ࠦ࠱ࠦࠢී")
      if bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠬࡵࡳࠨු")] == bstack111l1ll_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ෕"):
        bstack11l1111ll_opy_ += bstack111l1ll_opy_ (u"ࠢࡘ࡫ࡱࠤࠧූ")
      bstack11l1111ll_opy_ += bstack11l1lll11_opy_[bstack111l1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ෗")] or bstack111l1ll_opy_ (u"ࠩࠪෘ")
      return bstack11l1111ll_opy_
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1111l11l_opy_(bstack1ll11111ll_opy_):
  if bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠥࡨࡴࡴࡥࠣෙ"):
    return bstack111l1ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧේ")
  elif bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧෛ"):
    return bstack111l1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩො")
  elif bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢෝ"):
    return bstack111l1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨෞ")
  elif bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣෟ"):
    return bstack111l1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෠")
  elif bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ෡"):
    return bstack111l1ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ෢")
  elif bstack1ll11111ll_opy_ == bstack111l1ll_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢ෣"):
    return bstack111l1ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ෤")
  else:
    return bstack111l1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ෥") + bstack1l1l11l1l1_opy_(
      bstack1ll11111ll_opy_) + bstack111l1ll_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ෦")
def bstack111l1ll11_opy_(session):
  return bstack111l1ll_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ෧").format(
    session[bstack111l1ll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ෨")], bstack1llllllll1_opy_(session), bstack1111l11l_opy_(session[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ෩")]),
    bstack1111l11l_opy_(session[bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෪")]),
    bstack1l1l11l1l1_opy_(session[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ෫")] or session[bstack111l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ෬")] or bstack111l1ll_opy_ (u"ࠩࠪ෭")) + bstack111l1ll_opy_ (u"ࠥࠤࠧ෮") + (session[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෯")] or bstack111l1ll_opy_ (u"ࠬ࠭෰")),
    session[bstack111l1ll_opy_ (u"࠭࡯ࡴࠩ෱")] + bstack111l1ll_opy_ (u"ࠢࠡࠤෲ") + session[bstack111l1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬෳ")], session[bstack111l1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ෴")] or bstack111l1ll_opy_ (u"ࠪࠫ෵"),
    session[bstack111l1ll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ෶")] if session[bstack111l1ll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ෷")] else bstack111l1ll_opy_ (u"࠭ࠧ෸"))
@measure(event_name=EVENTS.bstack11llllll1l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def bstack1111l111l_opy_(sessions, bstack111ll1l11_opy_):
  try:
    bstack11ll1l1l11_opy_ = bstack111l1ll_opy_ (u"ࠢࠣ෹")
    if not os.path.exists(bstack1l11l1ll_opy_):
      os.mkdir(bstack1l11l1ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1ll_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭෺")), bstack111l1ll_opy_ (u"ࠩࡵࠫ෻")) as f:
      bstack11ll1l1l11_opy_ = f.read()
    bstack11ll1l1l11_opy_ = bstack11ll1l1l11_opy_.replace(bstack111l1ll_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ෼"), str(len(sessions)))
    bstack11ll1l1l11_opy_ = bstack11ll1l1l11_opy_.replace(bstack111l1ll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ෽"), bstack111ll1l11_opy_)
    bstack11ll1l1l11_opy_ = bstack11ll1l1l11_opy_.replace(bstack111l1ll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭෾"),
                                              sessions[0].get(bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ෿")) if sessions[0] else bstack111l1ll_opy_ (u"ࠧࠨ฀"))
    with open(os.path.join(bstack1l11l1ll_opy_, bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬก")), bstack111l1ll_opy_ (u"ࠩࡺࠫข")) as stream:
      stream.write(bstack11ll1l1l11_opy_.split(bstack111l1ll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧฃ"))[0])
      for session in sessions:
        stream.write(bstack111l1ll11_opy_(session))
      stream.write(bstack11ll1l1l11_opy_.split(bstack111l1ll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨค"))[1])
    logger.info(bstack111l1ll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨฅ").format(bstack1l11l1ll_opy_));
  except Exception as e:
    logger.debug(bstack1ll1ll1111_opy_.format(str(e)))
def bstack1l1111lll1_opy_(bstack11ll1ll1_opy_):
  global CONFIG
  try:
    host = bstack111l1ll_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩฆ") if bstack111l1ll_opy_ (u"ࠧࡢࡲࡳࠫง") in CONFIG else bstack111l1ll_opy_ (u"ࠨࡣࡳ࡭ࠬจ")
    user = CONFIG[bstack111l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫฉ")]
    key = CONFIG[bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ช")]
    bstack11ll1l11ll_opy_ = bstack111l1ll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪซ") if bstack111l1ll_opy_ (u"ࠬࡧࡰࡱࠩฌ") in CONFIG else (bstack111l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪญ") if CONFIG.get(bstack111l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫฎ")) else bstack111l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪฏ"))
    url = bstack111l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧฐ").format(user, key, host, bstack11ll1l11ll_opy_,
                                                                                bstack11ll1ll1_opy_)
    headers = {
      bstack111l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩฑ"): bstack111l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧฒ"),
    }
    proxies = bstack1111l1l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪณ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l1ll11l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11llll1l1l_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def get_build_link():
  global CONFIG
  global bstack1ll11l11_opy_
  try:
    if bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩด") in CONFIG:
      host = bstack111l1ll_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪต") if bstack111l1ll_opy_ (u"ࠨࡣࡳࡴࠬถ") in CONFIG else bstack111l1ll_opy_ (u"ࠩࡤࡴ࡮࠭ท")
      user = CONFIG[bstack111l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬธ")]
      key = CONFIG[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧน")]
      bstack11ll1l11ll_opy_ = bstack111l1ll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫบ") if bstack111l1ll_opy_ (u"࠭ࡡࡱࡲࠪป") in CONFIG else bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩผ")
      url = bstack111l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨฝ").format(user, key, host, bstack11ll1l11ll_opy_)
      headers = {
        bstack111l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨพ"): bstack111l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ฟ"),
      }
      if bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ภ") in CONFIG:
        params = {bstack111l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪม"): CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩย")], bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪร"): CONFIG[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪฤ")]}
      else:
        params = {bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧล"): CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฦ")]}
      proxies = bstack1111l1l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l111111l_opy_ = response.json()[0][bstack111l1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧว")]
        if bstack1l111111l_opy_:
          bstack111ll1l11_opy_ = bstack1l111111l_opy_[bstack111l1ll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩศ")].split(bstack111l1ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬษ"))[0] + bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨส") + bstack1l111111l_opy_[
            bstack111l1ll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫห")]
          logger.info(bstack1l1ll1lll_opy_.format(bstack111ll1l11_opy_))
          bstack1ll11l11_opy_ = bstack1l111111l_opy_[bstack111l1ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬฬ")]
          bstack11l11ll1_opy_ = CONFIG[bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭อ")]
          if bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ฮ") in CONFIG:
            bstack11l11ll1_opy_ += bstack111l1ll_opy_ (u"ࠬࠦࠧฯ") + CONFIG[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨะ")]
          if bstack11l11ll1_opy_ != bstack1l111111l_opy_[bstack111l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬั")]:
            logger.debug(bstack1l11lllll1_opy_.format(bstack1l111111l_opy_[bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭า")], bstack11l11ll1_opy_))
          return [bstack1l111111l_opy_[bstack111l1ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬำ")], bstack111ll1l11_opy_]
    else:
      logger.warn(bstack1l1ll11l1_opy_)
  except Exception as e:
    logger.debug(bstack1l1l11111l_opy_.format(str(e)))
  return [None, None]
def bstack1l1l1lll1l_opy_(url, bstack11ll1111l_opy_=False):
  global CONFIG
  global bstack11111lll1_opy_
  if not bstack11111lll1_opy_:
    hostname = bstack1ll11lll1_opy_(url)
    is_private = bstack1ll1ll111l_opy_(hostname)
    if (bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧิ") in CONFIG and not bstack1l1111111_opy_(CONFIG[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨี")])) and (is_private or bstack11ll1111l_opy_):
      bstack11111lll1_opy_ = hostname
def bstack1ll11lll1_opy_(url):
  return urlparse(url).hostname
def bstack1ll1ll111l_opy_(hostname):
  for bstack1l11l11l_opy_ in bstack1l1ll11ll_opy_:
    regex = re.compile(bstack1l11l11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l11ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l11111l11_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll11l11l_opy_
  bstack1l1l1l11l_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩึ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬื"), None))
  bstack1111111l_opy_ = getattr(driver, bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴุࠧ"), None) != True
  if not bstack1l1llll111_opy_.bstack11llll1ll1_opy_(CONFIG, bstack1ll11l11l_opy_) or (bstack1111111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack111l1ll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ูࠦ"))
    return {}
  try:
    logger.debug(bstack111l1ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸฺ࠭"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1111l111_opy_.bstack1l11111l1_opy_)
    return results
  except Exception:
    logger.error(bstack111l1ll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧ฻"))
    return {}
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll11l11l_opy_
  bstack1l1l1l11l_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ฼"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ฽"), None))
  bstack1111111l_opy_ = getattr(driver, bstack111l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭฾"), None) != True
  if not bstack1l1llll111_opy_.bstack11llll1ll1_opy_(CONFIG, bstack1ll11l11l_opy_) or (bstack1111111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack111l1ll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦ฿"))
    return {}
  try:
    logger.debug(bstack111l1ll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭เ"))
    logger.debug(perform_scan(driver))
    bstack1lll1ll1ll_opy_ = driver.execute_async_script(bstack1l1111l111_opy_.bstack1llll1llll_opy_)
    return bstack1lll1ll1ll_opy_
  except Exception:
    logger.error(bstack111l1ll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥแ"))
    return {}
@measure(event_name=EVENTS.bstack1l1ll1l11_opy_, stage=STAGE.SINGLE, bstack11l1111ll_opy_=bstack1ll1l1ll1l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1ll11l11l_opy_
  bstack1l1l1l11l_opy_ = not (bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧโ"), None) and bstack11llll11l_opy_(
          threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪใ"), None))
  bstack1111111l_opy_ = getattr(driver, bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬไ"), None) != True
  if not bstack1l1llll111_opy_.bstack11llll1ll1_opy_(CONFIG, bstack1ll11l11l_opy_) or (bstack1111111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack111l1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡵ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣๅ"))
    return {}
  try:
    bstack111ll11l1_opy_ = driver.execute_async_script(bstack1l1111l111_opy_.perform_scan, {bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧๆ"): kwargs.get(bstack111l1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩ็"), None) or bstack111l1ll_opy_ (u"่ࠩࠪ")})
    return bstack111ll11l1_opy_
  except Exception:
    logger.error(bstack111l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ้"))
    return {}
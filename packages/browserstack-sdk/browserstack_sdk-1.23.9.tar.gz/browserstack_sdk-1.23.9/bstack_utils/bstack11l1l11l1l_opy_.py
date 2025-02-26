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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l111l1l_opy_, bstack111l11l11l_opy_, bstack11ll1111_opy_, bstack11l1111l11_opy_, bstack11111111ll_opy_, bstack1lllll1llll_opy_, bstack1llll1111l1_opy_, bstack1ll111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll11l11ll1_opy_ import bstack1ll111lll11_opy_
import bstack_utils.bstack11llll11ll_opy_ as bstack1l111l1lll_opy_
from bstack_utils.bstack11l1ll11l1_opy_ import bstack11l111ll1_opy_
import bstack_utils.bstack111l1lll1l_opy_ as bstack1l1llll111_opy_
from bstack_utils.bstack1l1111l111_opy_ import bstack1l1111l111_opy_
from bstack_utils.bstack11l1ll1l1l_opy_ import bstack11l11ll11l_opy_
bstack1l1lll11ll1_opy_ = bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫឈ")
logger = logging.getLogger(__name__)
class bstack1lll1ll111_opy_:
    bstack1ll11l11ll1_opy_ = None
    bs_config = None
    bstack1llll1ll1_opy_ = None
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack111111llll_opy_, stage=STAGE.SINGLE)
    def launch(cls, bs_config, bstack1llll1ll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1llll1ll1_opy_ = bstack1llll1ll1_opy_
        try:
            cls.bstack1l1llll1l11_opy_()
            bstack111l111lll_opy_ = bstack111l111l1l_opy_(bs_config)
            bstack111l111ll1_opy_ = bstack111l11l11l_opy_(bs_config)
            data = bstack1l111l1lll_opy_.bstack1l1llllll11_opy_(bs_config, bstack1llll1ll1_opy_)
            config = {
                bstack111l1ll_opy_ (u"ࠬࡧࡵࡵࡪࠪញ"): (bstack111l111lll_opy_, bstack111l111ll1_opy_),
                bstack111l1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧដ"): cls.default_headers()
            }
            response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠧࡑࡑࡖࡘࠬឋ"), cls.request_url(bstack111l1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨឌ")), data, config)
            if response.status_code != 200:
                bstack1l1lllllll1_opy_ = response.json()
                if bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪឍ")] == False:
                    cls.bstack1l1lll1l1ll_opy_(bstack1l1lllllll1_opy_)
                    return
                cls.bstack1l1llll1ll1_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪណ")])
                cls.bstack1l1lll1lll1_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫត")])
                return None
            bstack1l1llllllll_opy_ = cls.bstack1l1lll1ll1l_opy_(response)
            return bstack1l1llllllll_opy_
        except Exception as error:
            logger.error(bstack111l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥថ").format(str(error)))
            return None
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def stop(cls, bstack1l1lllll111_opy_=None):
        if not bstack11l111ll1_opy_.on() and not bstack1l1llll111_opy_.on():
            return
        if os.environ.get(bstack111l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧទ")) == bstack111l1ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧធ") or os.environ.get(bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ន")) == bstack111l1ll_opy_ (u"ࠤࡱࡹࡱࡲࠢប"):
            logger.error(bstack111l1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ផ"))
            return {
                bstack111l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫព"): bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫភ"),
                bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧម"): bstack111l1ll_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬយ")
            }
        try:
            cls.bstack1ll11l11ll1_opy_.shutdown()
            data = {
                bstack111l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭រ"): bstack1ll111l1l_opy_()
            }
            if not bstack1l1lllll111_opy_ is None:
                data[bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ល")] = [{
                    bstack111l1ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪវ"): bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩឝ"),
                    bstack111l1ll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬឞ"): bstack1l1lllll111_opy_
                }]
            config = {
                bstack111l1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧស"): cls.default_headers()
            }
            bstack1lll1llll1l_opy_ = bstack111l1ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨហ").format(os.environ[bstack111l1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨឡ")])
            bstack1l1lll1llll_opy_ = cls.request_url(bstack1lll1llll1l_opy_)
            response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠩࡓ࡙࡙࠭អ"), bstack1l1lll1llll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l1ll_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤឣ"))
        except Exception as error:
            logger.error(bstack111l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣឤ") + str(error))
            return {
                bstack111l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬឥ"): bstack111l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬឦ"),
                bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨឧ"): str(error)
            }
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack1l1lll1ll1l_opy_(cls, response):
        bstack1l1lllllll1_opy_ = response.json()
        bstack1l1llllllll_opy_ = {}
        if bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠨ࡬ࡺࡸࠬឨ")) is None:
            os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪឩ")] = bstack111l1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨឪ")
        else:
            os.environ[bstack111l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬឫ")] = bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠬࡰࡷࡵࠩឬ"), bstack111l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫឭ"))
        os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬឮ")] = bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪឯ"), bstack111l1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧឰ"))
        logger.info(bstack111l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨឱ") + os.getenv(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩឲ")));
        if bstack11l111ll1_opy_.bstack1l1llll111l_opy_(cls.bs_config, cls.bstack1llll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ឳ"), bstack111l1ll_opy_ (u"࠭ࠧ឴"))) is True:
            bstack1l1llll1lll_opy_, bstack11lllll11_opy_, bstack1l1lllll1ll_opy_ = cls.bstack1l1lllll1l1_opy_(bstack1l1lllllll1_opy_)
            if bstack1l1llll1lll_opy_ != None and bstack11lllll11_opy_ != None:
                bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ឵")] = {
                    bstack111l1ll_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫា"): bstack1l1llll1lll_opy_,
                    bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫិ"): bstack11lllll11_opy_,
                    bstack111l1ll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧី"): bstack1l1lllll1ll_opy_
                }
            else:
                bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫឹ")] = {}
        else:
            bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬឺ")] = {}
        if bstack1l1llll111_opy_.bstack111l11ll1l_opy_(cls.bs_config) is True:
            bstack1l1llll1l1l_opy_, bstack11lllll11_opy_ = cls.bstack1l1lll1ll11_opy_(bstack1l1lllllll1_opy_)
            if bstack1l1llll1l1l_opy_ != None and bstack11lllll11_opy_ != None:
                bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ុ")] = {
                    bstack111l1ll_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫូ"): bstack1l1llll1l1l_opy_,
                    bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪួ"): bstack11lllll11_opy_,
                }
            else:
                bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩើ")] = {}
        else:
            bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪឿ")] = {}
        if bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫៀ")].get(bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧេ")) != None or bstack1l1llllllll_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ែ")].get(bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩៃ")) != None:
            cls.bstack1l1lll111l1_opy_(bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠨ࡬ࡺࡸࠬោ")), bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫៅ")))
        return bstack1l1llllllll_opy_
    @classmethod
    def bstack1l1lllll1l1_opy_(cls, bstack1l1lllllll1_opy_):
        if bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪំ")) == None:
            cls.bstack1l1llll1ll1_opy_()
            return [None, None, None]
        if bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫះ")][bstack111l1ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ៈ")] != True:
            cls.bstack1l1llll1ll1_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭៉")])
            return [None, None, None]
        logger.debug(bstack111l1ll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ៊"))
        os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ់")] = bstack111l1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ៌")
        if bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠪ࡮ࡼࡺࠧ៍")):
            os.environ[bstack111l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ៎")] = bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠬࡰࡷࡵࠩ៏")]
            os.environ[bstack111l1ll_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ័")] = json.dumps({
                bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ៑"): bstack111l111l1l_opy_(cls.bs_config),
                bstack111l1ll_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦ្ࠪ"): bstack111l11l11l_opy_(cls.bs_config)
            })
        if bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ៓")):
            os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ។")] = bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭៕")]
        if bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ៖")].get(bstack111l1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧៗ"), {}).get(bstack111l1ll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ៘")):
            os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ៙")] = str(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ៚")][bstack111l1ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ៛")][bstack111l1ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨៜ")])
        return [bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠬࡰࡷࡵࠩ៝")], bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ៞")], os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ៟")]]
    @classmethod
    def bstack1l1lll1ll11_opy_(cls, bstack1l1lllllll1_opy_):
        if bstack1l1lllllll1_opy_.get(bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ០")) == None:
            cls.bstack1l1lll1lll1_opy_()
            return [None, None]
        if bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ១")][bstack111l1ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ២")] != True:
            cls.bstack1l1lll1lll1_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៣")])
            return [None, None]
        if bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ៤")].get(bstack111l1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ៥")):
            logger.debug(bstack111l1ll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ៦"))
            parsed = json.loads(os.getenv(bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ៧"), bstack111l1ll_opy_ (u"ࠩࡾࢁࠬ៨")))
            capabilities = bstack1l111l1lll_opy_.bstack1l1lll1l11l_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ៩")][bstack111l1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ៪")][bstack111l1ll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៫")], bstack111l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ៬"), bstack111l1ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭៭"))
            bstack1l1llll1l1l_opy_ = capabilities[bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭៮")]
            os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ៯")] = bstack1l1llll1l1l_opy_
            parsed[bstack111l1ll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ៰")] = capabilities[bstack111l1ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ៱")]
            os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭៲")] = json.dumps(parsed)
            scripts = bstack1l111l1lll_opy_.bstack1l1lll1l11l_opy_(bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭៳")][bstack111l1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ៴")][bstack111l1ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ៵")], bstack111l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ៶"), bstack111l1ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫ៷"))
            bstack1l1111l111_opy_.bstack111l1l1111_opy_(scripts)
            commands = bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៸")][bstack111l1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭៹")][bstack111l1ll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ៺")].get(bstack111l1ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ៻"))
            bstack1l1111l111_opy_.bstack111l1l1l1l_opy_(commands)
            bstack1l1111l111_opy_.store()
        return [bstack1l1llll1l1l_opy_, bstack1l1lllllll1_opy_[bstack111l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ៼")]]
    @classmethod
    def bstack1l1llll1ll1_opy_(cls, response=None):
        os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ៽")] = bstack111l1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ៾")
        os.environ[bstack111l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ៿")] = bstack111l1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ᠀")
        os.environ[bstack111l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ᠁")] = bstack111l1ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ᠂")
        os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩ᠃")] = bstack111l1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ᠄")
        os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ᠅")] = bstack111l1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᠆")
        os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭᠇")] = bstack111l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᠈")
        cls.bstack1l1lll1l1ll_opy_(response, bstack111l1ll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ᠉"))
        return [None, None, None]
    @classmethod
    def bstack1l1lll1lll1_opy_(cls, response=None):
        os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᠊")] = bstack111l1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ᠋")
        os.environ[bstack111l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᠌")] = bstack111l1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ᠍")
        os.environ[bstack111l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᠎")] = bstack111l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ᠏")
        cls.bstack1l1lll1l1ll_opy_(response, bstack111l1ll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ᠐"))
        return [None, None, None]
    @classmethod
    def bstack1l1lll111l1_opy_(cls, bstack1l1lll111ll_opy_, bstack11lllll11_opy_):
        os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᠑")] = bstack1l1lll111ll_opy_
        os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᠒")] = bstack11lllll11_opy_
    @classmethod
    def bstack1l1lll1l1ll_opy_(cls, response=None, product=bstack111l1ll_opy_ (u"ࠥࠦ᠓")):
        if response == None:
            logger.error(product + bstack111l1ll_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨ᠔"))
        for error in response[bstack111l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ᠕")]:
            bstack1111111l11_opy_ = error[bstack111l1ll_opy_ (u"࠭࡫ࡦࡻࠪ᠖")]
            error_message = error[bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᠗")]
            if error_message:
                if bstack1111111l11_opy_ == bstack111l1ll_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢ᠘"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l1ll_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥ᠙") + product + bstack111l1ll_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ᠚"))
    @classmethod
    def bstack1l1llll1l11_opy_(cls):
        if cls.bstack1ll11l11ll1_opy_ is not None:
            return
        cls.bstack1ll11l11ll1_opy_ = bstack1ll111lll11_opy_(cls.bstack1l1llllll1l_opy_)
        cls.bstack1ll11l11ll1_opy_.start()
    @classmethod
    def bstack111lll1l11_opy_(cls):
        if cls.bstack1ll11l11ll1_opy_ is None:
            return
        cls.bstack1ll11l11ll1_opy_.shutdown()
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack1l1llllll1l_opy_(cls, bstack11l111111l_opy_, bstack1l1lll1l111_opy_=bstack111l1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ᠛")):
        config = {
            bstack111l1ll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᠜"): cls.default_headers()
        }
        logger.debug(bstack111l1ll_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨ᠝").format(bstack111l1ll_opy_ (u"ࠧ࠭ࠢࠪ᠞").join([event[bstack111l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᠟")] for event in bstack11l111111l_opy_])))
        response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᠠ"), cls.request_url(bstack1l1lll1l111_opy_), bstack11l111111l_opy_, config)
        bstack1111ll1ll1_opy_ = response.json()
    @classmethod
    def bstack1ll111lll_opy_(cls, bstack11l111111l_opy_, bstack1l1lll1l111_opy_=bstack111l1ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᠡ")):
        logger.debug(bstack111l1ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦᠢ").format(bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᠣ")]))
        if not bstack1l111l1lll_opy_.bstack1l1lll11l1l_opy_(bstack11l111111l_opy_[bstack111l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᠤ")]):
            logger.debug(bstack111l1ll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧᠥ").format(bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᠦ")]))
            return
        bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_.bstack1l1llll11ll_opy_(bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᠧ")], bstack11l111111l_opy_.get(bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᠨ")))
        if bstack1l11ll1ll_opy_ != None:
            if bstack11l111111l_opy_.get(bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᠩ")) != None:
                bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᠪ")][bstack111l1ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᠫ")] = bstack1l11ll1ll_opy_
            else:
                bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᠬ")] = bstack1l11ll1ll_opy_
        if bstack1l1lll1l111_opy_ == bstack111l1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᠭ"):
            cls.bstack1l1llll1l11_opy_()
            logger.debug(bstack111l1ll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧᠮ").format(bstack11l111111l_opy_[bstack111l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᠯ")]))
            cls.bstack1ll11l11ll1_opy_.add(bstack11l111111l_opy_)
        elif bstack1l1lll1l111_opy_ == bstack111l1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᠰ"):
            cls.bstack1l1llllll1l_opy_([bstack11l111111l_opy_], bstack1l1lll1l111_opy_)
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack11lll111l_opy_(cls, bstack11l11l1lll_opy_):
        bstack1ll11111111_opy_ = []
        for log in bstack11l11l1lll_opy_:
            bstack1l1llll1111_opy_ = {
                bstack111l1ll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᠱ"): bstack111l1ll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᠲ"),
                bstack111l1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᠳ"): log[bstack111l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᠴ")],
                bstack111l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᠵ"): log[bstack111l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᠶ")],
                bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᠷ"): {},
                bstack111l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᠸ"): log[bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᠹ")],
            }
            if bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᠺ") in log:
                bstack1l1llll1111_opy_[bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᠻ")] = log[bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᠼ")]
            elif bstack111l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᠽ") in log:
                bstack1l1llll1111_opy_[bstack111l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᠾ")] = log[bstack111l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᠿ")]
            bstack1ll11111111_opy_.append(bstack1l1llll1111_opy_)
        cls.bstack1ll111lll_opy_({
            bstack111l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᡀ"): bstack111l1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᡁ"),
            bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᡂ"): bstack1ll11111111_opy_
        })
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack1l1lll11l11_opy_(cls, steps):
        bstack1l1lll11lll_opy_ = []
        for step in steps:
            bstack1l1lllll11l_opy_ = {
                bstack111l1ll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᡃ"): bstack111l1ll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ᡄ"),
                bstack111l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᡅ"): step[bstack111l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᡆ")],
                bstack111l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᡇ"): step[bstack111l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᡈ")],
                bstack111l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡉ"): step[bstack111l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᡊ")],
                bstack111l1ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᡋ"): step[bstack111l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᡌ")]
            }
            if bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᡍ") in step:
                bstack1l1lllll11l_opy_[bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᡎ")] = step[bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᡏ")]
            elif bstack111l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᡐ") in step:
                bstack1l1lllll11l_opy_[bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᡑ")] = step[bstack111l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᡒ")]
            bstack1l1lll11lll_opy_.append(bstack1l1lllll11l_opy_)
        cls.bstack1ll111lll_opy_({
            bstack111l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᡓ"): bstack111l1ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᡔ"),
            bstack111l1ll_opy_ (u"࠭࡬ࡰࡩࡶࠫᡕ"): bstack1l1lll11lll_opy_
        })
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack1111lll1l_opy_(cls, screenshot):
        cls.bstack1ll111lll_opy_({
            bstack111l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᡖ"): bstack111l1ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᡗ"),
            bstack111l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᡘ"): [{
                bstack111l1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᡙ"): bstack111l1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ᡚ"),
                bstack111l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᡛ"): datetime.datetime.utcnow().isoformat() + bstack111l1ll_opy_ (u"࡚࠭ࠨᡜ"),
                bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᡝ"): screenshot[bstack111l1ll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᡞ")],
                bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᡟ"): screenshot[bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᡠ")]
            }]
        }, bstack1l1lll1l111_opy_=bstack111l1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᡡ"))
    @classmethod
    @bstack11l1111l11_opy_(class_method=True)
    def bstack1lllll1lll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll111lll_opy_({
            bstack111l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᡢ"): bstack111l1ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᡣ"),
            bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᡤ"): {
                bstack111l1ll_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᡥ"): cls.current_test_uuid(),
                bstack111l1ll_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᡦ"): cls.bstack11l1l1llll_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1ll1l11_opy_(cls, event: str, bstack11l111111l_opy_: bstack11l11ll11l_opy_):
        bstack111lllll1l_opy_ = {
            bstack111l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᡧ"): event,
            bstack11l111111l_opy_.bstack11l11lll1l_opy_(): bstack11l111111l_opy_.bstack11l11111l1_opy_(event)
        }
        cls.bstack1ll111lll_opy_(bstack111lllll1l_opy_)
        result = getattr(bstack11l111111l_opy_, bstack111l1ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᡨ"), None)
        if event == bstack111l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᡩ"):
            threading.current_thread().bstackTestMeta = {bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᡪ"): bstack111l1ll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᡫ")}
        elif event == bstack111l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡬ"):
            threading.current_thread().bstackTestMeta = {bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᡭ"): getattr(result, bstack111l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᡮ"), bstack111l1ll_opy_ (u"ࠫࠬᡯ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᡰ"), None) is None or os.environ[bstack111l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᡱ")] == bstack111l1ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᡲ")) and (os.environ.get(bstack111l1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᡳ"), None) is None or os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᡴ")] == bstack111l1ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᡵ")):
            return False
        return True
    @staticmethod
    def bstack1l1llll11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1ll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111l1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᡶ"): bstack111l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᡷ"),
            bstack111l1ll_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᡸ"): bstack111l1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ᡹")
        }
        if os.environ.get(bstack111l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᡺"), None):
            headers[bstack111l1ll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ᡻")] = bstack111l1ll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭᡼").format(os.environ[bstack111l1ll_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ᡽")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111l1ll_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ᡾").format(bstack1l1lll11ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ᡿"), None)
    @staticmethod
    def bstack11l1l1llll_opy_(driver):
        return {
            bstack11111111ll_opy_(): bstack1lllll1llll_opy_(driver)
        }
    @staticmethod
    def bstack1l1lll1l1l1_opy_(exception_info, report):
        return [{bstack111l1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᢀ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l1lll11_opy_(typename):
        if bstack111l1ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᢁ") in typename:
            return bstack111l1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᢂ")
        return bstack111l1ll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᢃ")
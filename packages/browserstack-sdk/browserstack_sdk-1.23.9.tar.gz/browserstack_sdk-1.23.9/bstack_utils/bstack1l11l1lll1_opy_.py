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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllll1ll1l_opy_, bstack1ll11lll1_opy_, bstack11llll11l_opy_, bstack1ll1ll111l_opy_, \
    bstack1llllll1ll1_opy_
from bstack_utils.measure import measure
def bstack1111ll1ll_opy_(bstack1ll111l1l1l_opy_):
    for driver in bstack1ll111l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.SINGLE)
def bstack11l1lllll1_opy_(driver, status, reason=bstack111l1ll_opy_ (u"ࠨ᜕ࠩ")):
    bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
    if bstack1ll11lll_opy_.bstack111ll11l1l_opy_():
        return
    bstack1lll11l1l_opy_ = bstack1l1l1ll1l1_opy_(bstack111l1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᜖"), bstack111l1ll_opy_ (u"ࠪࠫ᜗"), status, reason, bstack111l1ll_opy_ (u"ࠫࠬ᜘"), bstack111l1ll_opy_ (u"ࠬ࠭᜙"))
    driver.execute_script(bstack1lll11l1l_opy_)
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.SINGLE)
def bstack11ll111l11_opy_(page, status, reason=bstack111l1ll_opy_ (u"࠭ࠧ᜚")):
    try:
        if page is None:
            return
        bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
        if bstack1ll11lll_opy_.bstack111ll11l1l_opy_():
            return
        bstack1lll11l1l_opy_ = bstack1l1l1ll1l1_opy_(bstack111l1ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ᜛"), bstack111l1ll_opy_ (u"ࠨࠩ᜜"), status, reason, bstack111l1ll_opy_ (u"ࠩࠪ᜝"), bstack111l1ll_opy_ (u"ࠪࠫ᜞"))
        page.evaluate(bstack111l1ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᜟ"), bstack1lll11l1l_opy_)
    except Exception as e:
        print(bstack111l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᜠ"), e)
def bstack1l1l1ll1l1_opy_(type, name, status, reason, bstack1ll11l111l_opy_, bstack1llll11l11_opy_):
    bstack111l1111_opy_ = {
        bstack111l1ll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᜡ"): type,
        bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜢ"): {}
    }
    if type == bstack111l1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᜣ"):
        bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᜤ")][bstack111l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᜥ")] = bstack1ll11l111l_opy_
        bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᜦ")][bstack111l1ll_opy_ (u"ࠬࡪࡡࡵࡣࠪᜧ")] = json.dumps(str(bstack1llll11l11_opy_))
    if type == bstack111l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᜨ"):
        bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜩ")][bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᜪ")] = name
    if type == bstack111l1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᜫ"):
        bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᜬ")][bstack111l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᜭ")] = status
        if status == bstack111l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᜮ") and str(reason) != bstack111l1ll_opy_ (u"ࠨࠢᜯ"):
            bstack111l1111_opy_[bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᜰ")][bstack111l1ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᜱ")] = json.dumps(str(reason))
    bstack1l1l1lllll_opy_ = bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᜲ").format(json.dumps(bstack111l1111_opy_))
    return bstack1l1l1lllll_opy_
def bstack1l1l1lll1l_opy_(url, config, logger, bstack11ll1111l_opy_=False):
    hostname = bstack1ll11lll1_opy_(url)
    is_private = bstack1ll1ll111l_opy_(hostname)
    try:
        if is_private or bstack11ll1111l_opy_:
            file_path = bstack1lllll1ll1l_opy_(bstack111l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᜳ"), bstack111l1ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰ᜴ࠪ"), logger)
            if os.environ.get(bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ᜵")) and eval(
                    os.environ.get(bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ᜶"))):
                return
            if (bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᜷") in config and not config[bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᜸")]):
                os.environ[bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ᜹")] = str(True)
                bstack1ll111l1ll1_opy_ = {bstack111l1ll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ᜺"): hostname}
                bstack1llllll1ll1_opy_(bstack111l1ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᜻"), bstack111l1ll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ᜼"), bstack1ll111l1ll1_opy_, logger)
    except Exception as e:
        pass
def bstack1l111l1111_opy_(caps, bstack1ll111l1lll_opy_):
    if bstack111l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᜽") in caps:
        caps[bstack111l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᜾")][bstack111l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ᜿")] = True
        if bstack1ll111l1lll_opy_:
            caps[bstack111l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᝀ")][bstack111l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᝁ")] = bstack1ll111l1lll_opy_
    else:
        caps[bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᝂ")] = True
        if bstack1ll111l1lll_opy_:
            caps[bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᝃ")] = bstack1ll111l1lll_opy_
def bstack1ll11l1l1ll_opy_(bstack11l11l11l1_opy_):
    bstack1ll111l1l11_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᝄ"), bstack111l1ll_opy_ (u"ࠧࠨᝅ"))
    if bstack1ll111l1l11_opy_ == bstack111l1ll_opy_ (u"ࠨࠩᝆ") or bstack1ll111l1l11_opy_ == bstack111l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᝇ"):
        threading.current_thread().testStatus = bstack11l11l11l1_opy_
    else:
        if bstack11l11l11l1_opy_ == bstack111l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᝈ"):
            threading.current_thread().testStatus = bstack11l11l11l1_opy_
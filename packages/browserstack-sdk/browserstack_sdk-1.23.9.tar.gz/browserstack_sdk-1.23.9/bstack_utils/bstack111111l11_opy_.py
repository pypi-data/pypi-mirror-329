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
import re
from bstack_utils.bstack1l11l1lll1_opy_ import bstack1ll11l1l1ll_opy_
def bstack1ll11l1lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111l1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᛛ")):
        return bstack111l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᛜ")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᛝ")):
        return bstack111l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᛞ")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᛟ")):
        return bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᛠ")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᛡ")):
        return bstack111l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᛢ")
def bstack1ll11ll11l1_opy_(fixture_name):
    return bool(re.match(bstack111l1ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᛣ"), fixture_name))
def bstack1ll11l1ll1l_opy_(fixture_name):
    return bool(re.match(bstack111l1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᛤ"), fixture_name))
def bstack1ll11ll1111_opy_(fixture_name):
    return bool(re.match(bstack111l1ll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᛥ"), fixture_name))
def bstack1ll11l1llll_opy_(fixture_name):
    if fixture_name.startswith(bstack111l1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᛦ")):
        return bstack111l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᛧ"), bstack111l1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᛨ")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᛩ")):
        return bstack111l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᛪ"), bstack111l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ᛫")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᛬")):
        return bstack111l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᛭"), bstack111l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᛮ")
    elif fixture_name.startswith(bstack111l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᛯ")):
        return bstack111l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᛰ"), bstack111l1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᛱ")
    return None, None
def bstack1ll11l1l11l_opy_(hook_name):
    if hook_name in [bstack111l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᛲ"), bstack111l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᛳ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll11l1l111_opy_(hook_name):
    if hook_name in [bstack111l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᛴ"), bstack111l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᛵ")]:
        return bstack111l1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᛶ")
    elif hook_name in [bstack111l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᛷ"), bstack111l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᛸ")]:
        return bstack111l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ᛹")
    elif hook_name in [bstack111l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᛺"), bstack111l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ᛻")]:
        return bstack111l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ᛼")
    elif hook_name in [bstack111l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ᛽"), bstack111l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ᛾")]:
        return bstack111l1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ᛿")
    return hook_name
def bstack1ll11ll1l1l_opy_(node, scenario):
    if hasattr(node, bstack111l1ll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᜀ")):
        parts = node.nodeid.rsplit(bstack111l1ll_opy_ (u"ࠤ࡞ࠦᜁ"))
        params = parts[-1]
        return bstack111l1ll_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᜂ").format(scenario.name, params)
    return scenario.name
def bstack1ll11l1ll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l1ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᜃ")):
            examples = list(node.callspec.params[bstack111l1ll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᜄ")].values())
        return examples
    except:
        return []
def bstack1ll11ll1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll11ll111l_opy_(report):
    try:
        status = bstack111l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᜅ")
        if report.passed or (report.failed and hasattr(report, bstack111l1ll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᜆ"))):
            status = bstack111l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᜇ")
        elif report.skipped:
            status = bstack111l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᜈ")
        bstack1ll11l1l1ll_opy_(status)
    except:
        pass
def bstack111l11111_opy_(status):
    try:
        bstack1ll11l1l1l1_opy_ = bstack111l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᜉ")
        if status == bstack111l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᜊ"):
            bstack1ll11l1l1l1_opy_ = bstack111l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᜋ")
        elif status == bstack111l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᜌ"):
            bstack1ll11l1l1l1_opy_ = bstack111l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᜍ")
        bstack1ll11l1l1ll_opy_(bstack1ll11l1l1l1_opy_)
    except:
        pass
def bstack1ll11ll11ll_opy_(item=None, report=None, summary=None, extra=None):
    return
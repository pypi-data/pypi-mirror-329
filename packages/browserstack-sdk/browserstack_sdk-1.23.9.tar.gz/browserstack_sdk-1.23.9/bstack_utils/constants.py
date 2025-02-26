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
import re
from enum import Enum
bstack11lllll11l_opy_ = {
  bstack111l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ႔"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ႕"),
  bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ႖"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ႗"),
  bstack111l1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ႘"): bstack111l1ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ႙"),
  bstack111l1ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨႚ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩႛ"),
  bstack111l1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨႜ"): bstack111l1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬႝ"),
  bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ႞"): bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ႟"),
  bstack111l1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬႠ"): bstack111l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ⴁ"),
  bstack111l1ll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨႢ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨႣ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩႤ"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬႥ"),
  bstack111l1ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫႦ"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫႧ"),
  bstack111l1ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬႨ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬႩ"),
  bstack111l1ll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩႪ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩႫ"),
  bstack111l1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫႬ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫႭ"),
  bstack111l1ll_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧႮ"): bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧႯ"),
  bstack111l1ll_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧႰ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧႱ"),
  bstack111l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭Ⴒ"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭Ⴓ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨႴ"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႵ"),
  bstack111l1ll_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧႶ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧႷ"),
  bstack111l1ll_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨႸ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨႹ"),
  bstack111l1ll_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬႺ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬႻ"),
  bstack111l1ll_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩႼ"): bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩႽ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫႾ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫႿ"),
  bstack111l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪჀ"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪჁ"),
  bstack111l1ll_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧჂ"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧჃ"),
  bstack111l1ll_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩჄ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩჅ"),
  bstack111l1ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭჆"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭Ⴧ"),
  bstack111l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ჈"): bstack111l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭჉"),
  bstack111l1ll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ჊"): bstack111l1ll_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭჋"),
  bstack111l1ll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ჌"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪჍ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ჎"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫ჏"),
  bstack111l1ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧა"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧბ"),
  bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧგ"): bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪდ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬე"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬვ"),
  bstack111l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬზ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬთ"),
  bstack111l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩი"): bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩკ"),
  bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫლ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫმ"),
  bstack111l1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧნ"): bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧო"),
  bstack111l1ll_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪპ"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪჟ"),
  bstack111l1ll_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭რ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ს"),
  bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ტ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭უ"),
  bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧფ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧქ")
}
bstack11111lllll_opy_ = [
  bstack111l1ll_opy_ (u"ࠧࡰࡵࠪღ"),
  bstack111l1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫყ"),
  bstack111l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫშ"),
  bstack111l1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨჩ"),
  bstack111l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨც"),
  bstack111l1ll_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩძ"),
  bstack111l1ll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭წ"),
]
bstack1ll111111_opy_ = {
  bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩჭ"): [bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩხ"), bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫჯ")],
  bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ჰ"): bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧჱ"),
  bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨჲ"): bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩჳ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬჴ"): bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ჵ"),
  bstack111l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫჶ"): bstack111l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬჷ"),
  bstack111l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫჸ"): bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ჹ"),
  bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪჺ"): bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ჻"),
  bstack111l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬჼ"): bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ჽ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡵࡶࠧჾ"): [bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖ࡟ࡊࡆࠪჿ"), bstack111l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࠨᄀ")],
  bstack111l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᄁ"): bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡐࡔࡍࡌࡆࡘࡈࡐࠬᄂ"),
  bstack111l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᄃ"): bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᄄ"),
  bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᄅ"): bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠨᄆ"),
  bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᄇ"): bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡕࡓࡄࡒࡗࡈࡇࡌࡆࠩᄈ")
}
bstack11111111_opy_ = {
  bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᄉ"): [bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᄊ"), bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᄋ")],
  bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᄌ"): [bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧᄍ"), bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᄎ")],
  bstack111l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᄏ"): bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᄐ"),
  bstack111l1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᄑ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᄒ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᄓ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᄔ"),
  bstack111l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᄕ"): [bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩᄖ"), bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᄗ")],
  bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᄘ"): bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᄙ"),
  bstack111l1ll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᄚ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᄛ"),
  bstack111l1ll_opy_ (u"ࠬࡧࡰࡱࠩᄜ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩᄝ"),
  bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᄞ"): bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᄟ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄠ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄡ")
}
bstack1l1111l1l_opy_ = {
  bstack111l1ll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᄢ"): bstack111l1ll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄣ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᄤ"): [bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄥ"), bstack111l1ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᄦ")],
  bstack111l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᄧ"): bstack111l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᄨ"),
  bstack111l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᄩ"): bstack111l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᄪ"),
  bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᄫ"): [bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᄬ"), bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᄭ")],
  bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᄮ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᄯ"),
  bstack111l1ll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᄰ"): bstack111l1ll_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᄱ"),
  bstack111l1ll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᄲ"): [bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᄳ"), bstack111l1ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄴ")],
  bstack111l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᄵ"): [bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᄶ"), bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᄷ")]
}
bstack1lll111111_opy_ = [
  bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᄸ"),
  bstack111l1ll_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᄹ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᄺ"),
  bstack111l1ll_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨᄻ"),
  bstack111l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᄼ"),
  bstack111l1ll_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᄽ"),
  bstack111l1ll_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᄾ"),
  bstack111l1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᄿ"),
  bstack111l1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᅀ"),
  bstack111l1ll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᅁ"),
  bstack111l1ll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᅂ"),
  bstack111l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᅃ"),
]
bstack1ll1l1l1l1_opy_ = [
  bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᅄ"),
  bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᅅ"),
  bstack111l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᅆ"),
  bstack111l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᅇ"),
  bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅈ"),
  bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᅉ"),
  bstack111l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᅊ"),
  bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᅋ"),
  bstack111l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᅌ"),
  bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᅍ"),
  bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᅎ"),
  bstack111l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᅏ"),
  bstack111l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫᅐ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᅑ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᅒ"),
  bstack111l1ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᅓ"),
  bstack111l1ll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫᅔ"),
  bstack111l1ll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬᅕ"),
  bstack111l1ll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭ᅖ"),
  bstack111l1ll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧᅗ"),
  bstack111l1ll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨᅘ"),
  bstack111l1ll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩᅙ"),
  bstack111l1ll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪᅚ"),
  bstack111l1ll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫᅛ"),
  bstack111l1ll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬᅜ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᅝ"),
  bstack111l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᅞ"),
  bstack111l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᅟ"),
  bstack111l1ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᅠ"),
  bstack111l1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᅡ"),
  bstack111l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅢ")
]
bstack1111l1111l_opy_ = [
  bstack111l1ll_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᅣ"),
  bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᅤ"),
  bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᅥ"),
  bstack111l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᅦ"),
  bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡑࡴ࡬ࡳࡷ࡯ࡴࡺࠩᅧ"),
  bstack111l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᅨ"),
  bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡦ࡭ࠧᅩ"),
  bstack111l1ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᅪ"),
  bstack111l1ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᅫ"),
  bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᅬ"),
  bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᅭ"),
  bstack111l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᅮ"),
  bstack111l1ll_opy_ (u"ࠫࡴࡹࠧᅯ"),
  bstack111l1ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᅰ"),
  bstack111l1ll_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬᅱ"),
  bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᅲ"),
  bstack111l1ll_opy_ (u"ࠨࡴࡨ࡫࡮ࡵ࡮ࠨᅳ"),
  bstack111l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᅴ"),
  bstack111l1ll_opy_ (u"ࠪࡱࡦࡩࡨࡪࡰࡨࠫᅵ"),
  bstack111l1ll_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨᅶ"),
  bstack111l1ll_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅷ"),
  bstack111l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᅸ"),
  bstack111l1ll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ᅹ"),
  bstack111l1ll_opy_ (u"ࠨࡰࡲࡔࡦ࡭ࡥࡍࡱࡤࡨ࡙࡯࡭ࡦࡱࡸࡸࠬᅺ"),
  bstack111l1ll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᅻ"),
  bstack111l1ll_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᅼ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᅽ"),
  bstack111l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᅾ"),
  bstack111l1ll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᅿ"),
  bstack111l1ll_opy_ (u"ࠧ࡯ࡱࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠫᆀ"),
  bstack111l1ll_opy_ (u"ࠨࡥ࡫ࡩࡨࡱࡕࡓࡎࠪᆁ"),
  bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᆂ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡆࡳࡴࡱࡩࡦࡵࠪᆃ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡧࡰࡵࡷࡵࡩࡈࡸࡡࡴࡪࠪᆄ"),
  bstack111l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᆅ"),
  bstack111l1ll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᆆ"),
  bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࡚ࡪࡸࡳࡪࡱࡱࠫᆇ"),
  bstack111l1ll_opy_ (u"ࠨࡰࡲࡆࡱࡧ࡮࡬ࡒࡲࡰࡱ࡯࡮ࡨࠩᆈ"),
  bstack111l1ll_opy_ (u"ࠩࡰࡥࡸࡱࡓࡦࡰࡧࡏࡪࡿࡳࠨᆉ"),
  bstack111l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡏࡳ࡬ࡹࠧᆊ"),
  bstack111l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡍࡩ࠭ᆋ"),
  bstack111l1ll_opy_ (u"ࠬࡪࡥࡥ࡫ࡦࡥࡹ࡫ࡤࡅࡧࡹ࡭ࡨ࡫ࠧᆌ"),
  bstack111l1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡖࡡࡳࡣࡰࡷࠬᆍ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡪࡲࡲࡪࡔࡵ࡮ࡤࡨࡶࠬᆎ"),
  bstack111l1ll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᆏ"),
  bstack111l1ll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡏࡱࡶ࡬ࡳࡳࡹࠧᆐ"),
  bstack111l1ll_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨᆑ"),
  bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᆒ"),
  bstack111l1ll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩᆓ"),
  bstack111l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡈࡩࡰ࡯ࡨࡸࡷ࡯ࡣࠨᆔ"),
  bstack111l1ll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࡜࠲ࠨᆕ"),
  bstack111l1ll_opy_ (u"ࠨ࡯࡬ࡨࡘ࡫ࡳࡴ࡫ࡲࡲࡎࡴࡳࡵࡣ࡯ࡰࡆࡶࡰࡴࠩᆖ"),
  bstack111l1ll_opy_ (u"ࠩࡨࡷࡵࡸࡥࡴࡵࡲࡗࡪࡸࡶࡦࡴࠪᆗ"),
  bstack111l1ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᆘ"),
  bstack111l1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡉࡤࡱࠩᆙ"),
  bstack111l1ll_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᆚ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡺࡰࡦࡘ࡮ࡳࡥࡘ࡫ࡷ࡬ࡓ࡚ࡐࠨᆛ"),
  bstack111l1ll_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᆜ"),
  bstack111l1ll_opy_ (u"ࠨࡩࡳࡷࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᆝ"),
  bstack111l1ll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᆞ"),
  bstack111l1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᆟ"),
  bstack111l1ll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࡆ࡬ࡦࡴࡧࡦࡌࡤࡶࠬᆠ"),
  bstack111l1ll_opy_ (u"ࠬࡾ࡭ࡴࡌࡤࡶࠬᆡ"),
  bstack111l1ll_opy_ (u"࠭ࡸ࡮ࡺࡍࡥࡷ࠭ᆢ"),
  bstack111l1ll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᆣ"),
  bstack111l1ll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᆤ"),
  bstack111l1ll_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᆥ"),
  bstack111l1ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ᆦ"),
  bstack111l1ll_opy_ (u"ࠫࡦࡶࡰࡗࡧࡵࡷ࡮ࡵ࡮ࠨᆧ"),
  bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᆨ"),
  bstack111l1ll_opy_ (u"࠭ࡲࡦࡵ࡬࡫ࡳࡇࡰࡱࠩᆩ"),
  bstack111l1ll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࡶࠫᆪ"),
  bstack111l1ll_opy_ (u"ࠨࡥࡤࡲࡦࡸࡹࠨᆫ"),
  bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᆬ"),
  bstack111l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᆭ"),
  bstack111l1ll_opy_ (u"ࠫ࡮࡫ࠧᆮ"),
  bstack111l1ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᆯ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᆰ"),
  bstack111l1ll_opy_ (u"ࠧࡲࡷࡨࡹࡪ࠭ᆱ"),
  bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪᆲ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡴࡵ࡙ࡴࡰࡴࡨࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠪᆳ"),
  bstack111l1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡆࡥࡲ࡫ࡲࡢࡋࡰࡥ࡬࡫ࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩᆴ"),
  bstack111l1ll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡇࡻࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧᆵ"),
  bstack111l1ll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡌࡲࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᆶ"),
  bstack111l1ll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᆷ"),
  bstack111l1ll_opy_ (u"ࠧࡳࡧࡶࡩࡷࡼࡥࡅࡧࡹ࡭ࡨ࡫ࠧᆸ"),
  bstack111l1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᆹ"),
  bstack111l1ll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫᆺ"),
  bstack111l1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡥࡸࡹࡣࡰࡦࡨࠫᆻ"),
  bstack111l1ll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡍࡴࡹࡄࡦࡸ࡬ࡧࡪ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᆼ"),
  bstack111l1ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬᆽ"),
  bstack111l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡰࡱ࡮ࡨࡔࡦࡿࠧᆾ"),
  bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᆿ"),
  bstack111l1ll_opy_ (u"ࠨࡹࡧ࡭ࡴ࡙ࡥࡳࡸ࡬ࡧࡪ࠭ᇀ"),
  bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᇁ"),
  bstack111l1ll_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷࡇࡷࡵࡳࡴࡕ࡬ࡸࡪ࡚ࡲࡢࡥ࡮࡭ࡳ࡭ࠧᇂ"),
  bstack111l1ll_opy_ (u"ࠫ࡭࡯ࡧࡩࡅࡲࡲࡹࡸࡡࡴࡶࠪᇃ"),
  bstack111l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡕࡸࡥࡧࡧࡵࡩࡳࡩࡥࡴࠩᇄ"),
  bstack111l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩᇅ"),
  bstack111l1ll_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᇆ"),
  bstack111l1ll_opy_ (u"ࠨࡴࡨࡱࡴࡼࡥࡊࡑࡖࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࡍࡱࡦࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᇇ"),
  bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫᇈ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᇉ"),
  bstack111l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᇊ"),
  bstack111l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᇋ"),
  bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᇌ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᇍ"),
  bstack111l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᇎ"),
  bstack111l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᇏ"),
  bstack111l1ll_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ᇐ")
]
bstack11l1lllll_opy_ = {
  bstack111l1ll_opy_ (u"ࠫࡻ࠭ᇑ"): bstack111l1ll_opy_ (u"ࠬࡼࠧᇒ"),
  bstack111l1ll_opy_ (u"࠭ࡦࠨᇓ"): bstack111l1ll_opy_ (u"ࠧࡧࠩᇔ"),
  bstack111l1ll_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᇕ"): bstack111l1ll_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᇖ"),
  bstack111l1ll_opy_ (u"ࠪࡳࡳࡲࡹࡢࡷࡷࡳࡲࡧࡴࡦࠩᇗ"): bstack111l1ll_opy_ (u"ࠫࡴࡴ࡬ࡺࡃࡸࡸࡴࡳࡡࡵࡧࠪᇘ"),
  bstack111l1ll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᇙ"): bstack111l1ll_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪᇚ"),
  bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪᇛ"): bstack111l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᇜ"),
  bstack111l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬᇝ"): bstack111l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᇞ"),
  bstack111l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᇟ"): bstack111l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᇠ"),
  bstack111l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᇡ"): bstack111l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᇢ"),
  bstack111l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᇣ"): bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᇤ"),
  bstack111l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᇥ"): bstack111l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬᇦ"),
  bstack111l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᇧ"): bstack111l1ll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᇨ"),
  bstack111l1ll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᇩ"): bstack111l1ll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᇪ"),
  bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᇫ"): bstack111l1ll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᇬ"),
  bstack111l1ll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᇭ"): bstack111l1ll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᇮ"),
  bstack111l1ll_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᇯ"): bstack111l1ll_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᇰ"),
  bstack111l1ll_opy_ (u"ࠨࡲࡤࡧ࡫࡯࡬ࡦࠩᇱ"): bstack111l1ll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᇲ"),
  bstack111l1ll_opy_ (u"ࠪࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᇳ"): bstack111l1ll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᇴ"),
  bstack111l1ll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᇵ"): bstack111l1ll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᇶ"),
  bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᇷ"): bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᇸ"),
  bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᇹ"): bstack111l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᇺ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ᇻ"): bstack111l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡰࡦࡣࡷࡩࡷ࠭ᇼ")
}
bstack11111ll111_opy_ = bstack111l1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨ࡫ࡷ࡬ࡺࡨ࠮ࡤࡱࡰ࠳ࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯࠯ࡳࡧ࡯ࡩࡦࡹࡥࡴ࠱࡯ࡥࡹ࡫ࡳࡵ࠱ࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᇽ")
bstack111111lll1_opy_ = bstack111l1ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠯ࡩࡧࡤࡰࡹ࡮ࡣࡩࡧࡦ࡯ࠧᇾ")
bstack11lll1l11_opy_ = bstack111l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡨࡨࡸ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡶࡩࡳࡪ࡟ࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦᇿ")
bstack111111l1l_opy_ = bstack111l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡻࡩ࠵ࡨࡶࡤࠪሀ")
bstack1lllllllll_opy_ = bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧ࠭ሁ")
bstack1llll11l1_opy_ = bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨሂ")
bstack11111l11ll_opy_ = {
  bstack111l1ll_opy_ (u"ࠬࡩࡲࡪࡶ࡬ࡧࡦࡲࠧሃ"): 50,
  bstack111l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬሄ"): 40,
  bstack111l1ll_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨህ"): 30,
  bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ሆ"): 20,
  bstack111l1ll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨሇ"): 10
}
bstack1lll1ll11_opy_ = bstack11111l11ll_opy_[bstack111l1ll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨለ")]
bstack1l1lllll_opy_ = bstack111l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪሉ")
bstack1ll111l1_opy_ = bstack111l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪሊ")
bstack1l11l11l1_opy_ = bstack111l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬላ")
bstack1l1lll1l1_opy_ = bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ሌ")
bstack11l1ll1ll_opy_ = bstack111l1ll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡲࡩࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡲࡤࡧࡰࡧࡧࡦࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭ል")
bstack11111l1l11_opy_ = [bstack111l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪሎ"), bstack111l1ll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪሏ")]
bstack11111l1lll_opy_ = [bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧሐ"), bstack111l1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧሑ")]
bstack11ll111ll1_opy_ = re.compile(bstack111l1ll_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬሒ"))
bstack1lll11ll11_opy_ = [
  bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨሓ"),
  bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪሔ"),
  bstack111l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ሕ"),
  bstack111l1ll_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧሖ"),
  bstack111l1ll_opy_ (u"ࠫࡦࡶࡰࠨሗ"),
  bstack111l1ll_opy_ (u"ࠬࡻࡤࡪࡦࠪመ"),
  bstack111l1ll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨሙ"),
  bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧሚ"),
  bstack111l1ll_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ማ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧሜ"),
  bstack111l1ll_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫም"), bstack111l1ll_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧሞ"),
  bstack111l1ll_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨሟ"),
  bstack111l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬሠ"),
  bstack111l1ll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫሡ"),
  bstack111l1ll_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫሢ"),
  bstack111l1ll_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪሣ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨሤ"), bstack111l1ll_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨሥ"), bstack111l1ll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧሦ"), bstack111l1ll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧሧ"), bstack111l1ll_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩረ"),
  bstack111l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ሩ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ሪ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬራ"), bstack111l1ll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨሬ"),
  bstack111l1ll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪር"),
  bstack111l1ll_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧሮ"),
  bstack111l1ll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭ሯ"),
  bstack111l1ll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩሰ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧሱ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡻࡪࠧሲ"), bstack111l1ll_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧሳ"), bstack111l1ll_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧሴ"), bstack111l1ll_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧስ"),
  bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬሶ"), bstack111l1ll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧሷ"), bstack111l1ll_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬሸ"),
  bstack111l1ll_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬሹ"), bstack111l1ll_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩሺ"),
  bstack111l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧሻ"), bstack111l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩሼ"), bstack111l1ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬሽ"), bstack111l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪሾ"), bstack111l1ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ሿ"),
  bstack111l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ቀ"), bstack111l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨቁ"),
  bstack111l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧቂ"),
  bstack111l1ll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫቃ"),
  bstack111l1ll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭ቄ"), bstack111l1ll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩቅ"), bstack111l1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧቆ"), bstack111l1ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ቇ"),
  bstack111l1ll_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩቈ"),
  bstack111l1ll_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ቉"), bstack111l1ll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ቊ"),
  bstack111l1ll_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧቋ"),
  bstack111l1ll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪቌ"),
  bstack111l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫቍ"),
  bstack111l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ቎"),
  bstack111l1ll_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ቏"),
  bstack111l1ll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫቐ"),
  bstack111l1ll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧቑ"),
  bstack111l1ll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭ቒ"),
  bstack111l1ll_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬቓ"),
  bstack111l1ll_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭ቔ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫቕ"),
  bstack111l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪቖ"),
  bstack111l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ቗"),
  bstack111l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭ቘ"),
  bstack111l1ll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ቙"),
  bstack111l1ll_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬቚ"),
  bstack111l1ll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩቛ"),
  bstack111l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧቜ"), bstack111l1ll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨቝ"), bstack111l1ll_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ቞"),
  bstack111l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ቟"),
  bstack111l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫበ"),
  bstack111l1ll_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪቡ"),
  bstack111l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫቢ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧባ"),
  bstack111l1ll_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨቤ"),
  bstack111l1ll_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨብ"), bstack111l1ll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬቦ"), bstack111l1ll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪቧ"),
  bstack111l1ll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨቨ"),
  bstack111l1ll_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪቩ"),
  bstack111l1ll_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬቪ"),
  bstack111l1ll_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫቫ"),
  bstack111l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨቬ"), bstack111l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬቭ"),
  bstack111l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪቮ"), bstack111l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬቯ"),
  bstack111l1ll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩተ"),
  bstack111l1ll_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩቱ"),
  bstack111l1ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧቲ"), bstack111l1ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩታ"), bstack111l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪቴ"), bstack111l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧት"),
  bstack111l1ll_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨቶ"),
  bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪቷ"),
  bstack111l1ll_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ቸ"),
  bstack111l1ll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫቹ"),
  bstack111l1ll_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩቺ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨቻ"),
  bstack111l1ll_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨቼ"), bstack111l1ll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩች"),
  bstack111l1ll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬቾ"),
  bstack111l1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪቿ"),
  bstack111l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬኀ"),
  bstack111l1ll_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬኁ"),
  bstack111l1ll_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨኂ"),
  bstack111l1ll_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪኃ"),
  bstack111l1ll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩኄ"),
  bstack111l1ll_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪኅ"),
  bstack111l1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪኆ"),
  bstack111l1ll_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩኇ"),
  bstack111l1ll_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪኈ"),
  bstack111l1ll_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ኉"),
  bstack111l1ll_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭ኊ"),
  bstack111l1ll_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪኋ"),
  bstack111l1ll_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫኌ"),
  bstack111l1ll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭ኍ"),
  bstack111l1ll_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬ኎"),
  bstack111l1ll_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭኏"),
  bstack111l1ll_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪነ"),
  bstack111l1ll_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭ኑ"),
  bstack111l1ll_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫኒ"),
  bstack111l1ll_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬና"), bstack111l1ll_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪኔ"),
  bstack111l1ll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨን"), bstack111l1ll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭ኖ"),
  bstack111l1ll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫኗ"),
  bstack111l1ll_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪኘ"),
  bstack111l1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪኙ"),
  bstack111l1ll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭ኚ"), bstack111l1ll_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭ኛ"),
  bstack111l1ll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧኜ"),
  bstack111l1ll_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪኝ"),
  bstack111l1ll_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭ኞ"),
  bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨኟ"),
  bstack111l1ll_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪአ"),
  bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬኡ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨኢ"),
  bstack111l1ll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪኣ"),
  bstack111l1ll_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧኤ"),
  bstack111l1ll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬእ"), bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫኦ"),
  bstack111l1ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨኧ"),
  bstack111l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬከ")
]
bstack1ll111lll1_opy_ = bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩኩ")
bstack1lll1l1lll_opy_ = [bstack111l1ll_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩኪ"), bstack111l1ll_opy_ (u"ࠬ࠴ࡡࡢࡤࠪካ"), bstack111l1ll_opy_ (u"࠭࠮ࡪࡲࡤࠫኬ")]
bstack111111ll1_opy_ = [bstack111l1ll_opy_ (u"ࠧࡪࡦࠪክ"), bstack111l1ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ኮ"), bstack111l1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬኯ"), bstack111l1ll_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩኰ")]
bstack11lll11ll_opy_ = {
  bstack111l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ኱"): bstack111l1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኲ"),
  bstack111l1ll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧኳ"): bstack111l1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬኴ"),
  bstack111l1ll_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ኵ"): bstack111l1ll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ኶"),
  bstack111l1ll_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭኷"): bstack111l1ll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኸ"),
  bstack111l1ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬኹ"): bstack111l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧኺ")
}
bstack111111111_opy_ = [
  bstack111l1ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬኻ"),
  bstack111l1ll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ኼ"),
  bstack111l1ll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኽ"),
  bstack111l1ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩኾ"),
  bstack111l1ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ኿"),
]
bstack11llll11l1_opy_ = bstack1ll1l1l1l1_opy_ + bstack1111l1111l_opy_ + bstack1lll11ll11_opy_
bstack1l1ll11ll_opy_ = [
  bstack111l1ll_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪዀ"),
  bstack111l1ll_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧ዁"),
  bstack111l1ll_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ዂ"),
  bstack111l1ll_opy_ (u"ࠨࡠ࠴࠴࠳࠭ዃ"),
  bstack111l1ll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨዄ"),
  bstack111l1ll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩዅ"),
  bstack111l1ll_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪ዆"),
  bstack111l1ll_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ዇")
]
bstack1111l11111_opy_ = bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧወ")
bstack1l1lll111_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭ዉ")
bstack11ll111l_opy_ = [ bstack111l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪዊ") ]
bstack111l1lll_opy_ = [ bstack111l1ll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨዋ") ]
bstack1llll1lll1_opy_ = [bstack111l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧዌ")]
bstack1ll111l11l_opy_ = [ bstack111l1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫው") ]
bstack1l1l111l_opy_ = bstack111l1ll_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧዎ")
bstack1ll11l1ll1_opy_ = bstack111l1ll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩዏ")
bstack1l111l1l_opy_ = bstack111l1ll_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫዐ")
bstack11lllll1ll_opy_ = bstack111l1ll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧዑ")
bstack11l1l11l_opy_ = [
  bstack111l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭ዒ"),
  bstack111l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪዓ"),
  bstack111l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬዔ"),
  bstack111l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫዕ"),
  bstack111l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪዖ"),
  bstack111l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ዗"),
  bstack111l1ll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨዘ"),
  bstack111l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫዙ"),
  bstack111l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬዚ"),
  bstack111l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬዛ"),
  bstack111l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ዜ"),
  bstack111l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬዝ"),
  bstack111l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪዞ"),
  bstack111l1ll_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩዟ"),
  bstack111l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ዠ"),
  bstack111l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪዡ"),
  bstack111l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧዢ"),
  bstack111l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬዣ"),
  bstack111l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧዤ"),
  bstack111l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ዥ"),
  bstack111l1ll_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧዦ"),
]
bstack1l11l1ll_opy_ = bstack111l1ll_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧዧ")
bstack11l1llll_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠪࢂࠬየ")), bstack111l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫዩ"), bstack111l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫዪ"))
bstack1111lll1l1_opy_ = bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧያ")
bstack11111ll1l1_opy_ = [ bstack111l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧዬ"), bstack111l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧይ"), bstack111l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨዮ"), bstack111l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪዯ")]
bstack111l1l111_opy_ = [ bstack111l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫደ"), bstack111l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫዱ"), bstack111l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬዲ"), bstack111l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧዳ") ]
bstack111lllll11_opy_ = {
  bstack111l1ll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ዴ"): bstack111l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩድ"),
  bstack111l1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨዶ"): bstack111l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዷ"),
  bstack111l1ll_opy_ (u"࡙ࠬࡋࡊࡒࠪዸ"): bstack111l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧዹ")
}
bstack1ll1l1llll_opy_ = [
  bstack111l1ll_opy_ (u"ࠢࡨࡧࡷࠦዺ"),
  bstack111l1ll_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣዻ"),
  bstack111l1ll_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧዼ"),
  bstack111l1ll_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦዽ"),
  bstack111l1ll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥዾ"),
  bstack111l1ll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤዿ"),
  bstack111l1ll_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨጀ"),
  bstack111l1ll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦጁ"),
  bstack111l1ll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦጂ"),
  bstack111l1ll_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣጃ"),
  bstack111l1ll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦጄ"),
  bstack111l1ll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦጅ"),
  bstack111l1ll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥጆ"),
  bstack111l1ll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧጇ"),
  bstack111l1ll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧገ"),
  bstack111l1ll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨጉ"),
  bstack111l1ll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨጊ"),
  bstack111l1ll_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤጋ"),
  bstack111l1ll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨጌ")
]
bstack111111ll1l_opy_ = [
  bstack111l1ll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦግ"),
  bstack111l1ll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጎ"),
  bstack111l1ll_opy_ (u"ࠢࡢࡷࡷࡳࠧጏ"),
  bstack111l1ll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣጐ"),
  bstack111l1ll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ጑")
]
bstack1l1l1ll11_opy_ = {
  bstack111l1ll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤጒ"): [bstack111l1ll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥጓ")],
  bstack111l1ll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤጔ"): [bstack111l1ll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጕ")],
  bstack111l1ll_opy_ (u"ࠢࡢࡷࡷࡳࠧ጖"): [bstack111l1ll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ጗"), bstack111l1ll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧጘ"), bstack111l1ll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢጙ"), bstack111l1ll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥጚ")],
  bstack111l1ll_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧጛ"): [bstack111l1ll_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨጜ")],
  bstack111l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤጝ"): [bstack111l1ll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥጞ")],
}
bstack11111lll1l_opy_ = {
  bstack111l1ll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣጟ"): bstack111l1ll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤጠ"),
  bstack111l1ll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣጡ"): bstack111l1ll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤጢ"),
  bstack111l1ll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥጣ"): bstack111l1ll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤጤ"),
  bstack111l1ll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦጥ"): bstack111l1ll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦጦ"),
  bstack111l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧጧ"): bstack111l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨጨ")
}
bstack11l111l11l_opy_ = {
  bstack111l1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩጩ"): bstack111l1ll_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫጪ"),
  bstack111l1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪጫ"): bstack111l1ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩጬ"),
  bstack111l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧጭ"): bstack111l1ll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧጮ"),
  bstack111l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨጯ"): bstack111l1ll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬጰ")
}
bstack11111lll11_opy_ = 65536
bstack11111l11l1_opy_ = bstack111l1ll_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧጱ")
bstack11111ll1ll_opy_ = [
      bstack111l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩጲ"), bstack111l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጳ"), bstack111l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬጴ"), bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧጵ"), bstack111l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ጶ"),
      bstack111l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨጷ"), bstack111l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩጸ"), bstack111l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨጹ"), bstack111l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩጺ"),
      bstack111l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጻ"), bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጼ"), bstack111l1ll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧጽ")
    ]
bstack1111l11l1l_opy_= {
  bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩጾ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪጿ"),
  bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫፀ"): bstack111l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬፁ"),
  bstack111l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨፂ"): bstack111l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧፃ"),
  bstack111l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫፄ"): bstack111l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬፅ"),
  bstack111l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩፆ"): bstack111l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪፇ"),
  bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪፈ"): bstack111l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫፉ"),
  bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ፊ"): bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧፋ"),
  bstack111l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩፌ"): bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪፍ"),
  bstack111l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪፎ"): bstack111l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫፏ"),
  bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧፐ"): bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨፑ"),
  bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨፒ"): bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩፓ"),
  bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪፔ"): bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫፕ"),
  bstack111l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪፖ"): bstack111l1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫፗ"),
  bstack111l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧፘ"): bstack111l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ፙ"),
  bstack111l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧፚ"): bstack111l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ፛"),
  bstack111l1ll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ፜"): bstack111l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ፝"),
  bstack111l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ፞"): bstack111l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ፟"),
  bstack111l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ፠"): bstack111l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ፡"),
  bstack111l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ።"): bstack111l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ፣"),
  bstack111l1ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ፤"): bstack111l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ፥"),
  bstack111l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ፦"): bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ፧"),
  bstack111l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ፨"): bstack111l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭፩"),
  bstack111l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ፪"): bstack111l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ፫"),
  bstack111l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭፬"): bstack111l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ፭"),
  bstack111l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ፮"): bstack111l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ፯")
}
bstack11111llll1_opy_ = [bstack111l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭፰"), bstack111l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭፱")]
bstack1l1ll11l11_opy_ = bstack111l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳࡬ࡸࡩࡥࡵ࠲ࠦ፲")
bstack1ll1ll1l1l_opy_ = bstack111l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫ࡷ࡯ࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࠣ፳")
bstack1l11l1111_opy_ = bstack111l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠦ፴")
class EVENTS(Enum):
  bstack1111l111ll_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ፵")
  bstack1l1l1l1l1_opy_ = bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࠪ፶") # final bstack11111l1l1l_opy_
  bstack11111l1ll1_opy_ = bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࡭ࡱࡪࡷࠬ፷")
  bstack11111l111_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ፸")
  bstack11llll1l1l_opy_ = bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ፹")
  bstack111111llll_opy_ = bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨࠧ፺")
  bstack111111l1ll_opy_ = bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨ፻")
  bstack1ll1l1lll1_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭፼")
  bstack111l1111ll_opy_ = bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡴࡣࡹࡩ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭፽")
  bstack1l1ll1l11_opy_ = bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡲࡨࡶ࡫ࡵࡲ࡮ࡵࡦࡥࡳ࠭፾")
  bstack1l1lll1l1l_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀ࡬ࡰࡥࡤࡰࠬ፿")
  bstack1l1l1l111l_opy_ = bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡦࡶࡰ࠮ࡷࡳࡰࡴࡧࡤࠨᎀ")
  bstack11llllll1l_opy_ = bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡥ࡬࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹࠧᎁ")
  bstack1ll11ll1l1_opy_ = bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫᎂ")
  bstack1l11111l11_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫᎃ")
  bstack111111l1l1_opy_ = bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹࠨᎄ")
  SDK_PERCY_SCREENSHOT = bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᎅ")
  bstack11lll111l1_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡴࡶࡤࡸࡺࡹࠧᎆ")
  bstack11llll111l_opy_ = bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᎇ")
  bstack1111l111l1_opy_ = bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡱࡻࡽ࠲ࡹࡥࡵࡷࡳࠫᎈ")
  bstack111lllll1_opy_ = bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡷࡹࡵ࠭ᎉ")
  bstack111111ll11_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡰࡤࡴࡸ࡮࡯ࡵࠩᎊ") # not bstack11111ll11l_opy_ in python
  bstack1l11l1ll1l_opy_ = bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡴࡹ࡮ࡺࠧᎋ") # used in bstack11111l1111_opy_
  bstack1l1l1l1lll_opy_ = bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧᎌ") # used in bstack11111l1111_opy_
  bstack1l11llll1_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩᎍ")
  bstack1ll11111l1_opy_ = bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭ᎎ")
  bstack1lll111lll_opy_ = bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭ᎏ") #
  bstack1lll11l11l_opy_ = bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭᎐")
  bstack1l1l11lll_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭᎑")
  bstack1lll1l1l1_opy_ = bstack111l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫ᎒")
  bstack11l1111l1_opy_ = bstack111l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭᎓")
  bstack11lll111ll_opy_ = bstack111l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᎔")
  bstack11ll1l1ll_opy_ = bstack111l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ᎕")
  bstack1111l11l11_opy_ = bstack111l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ᎖")
  bstack11111l111l_opy_ = bstack111l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨ᎗")
class STAGE(Enum):
  bstack1l1l1ll1_opy_ = bstack111l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ᎘")
  END = bstack111l1ll_opy_ (u"ࠬ࡫࡮ࡥࠩ᎙")
  SINGLE = bstack111l1ll_opy_ (u"࠭ࡳࡪࡰࡪࡰࡪ࠭᎚")
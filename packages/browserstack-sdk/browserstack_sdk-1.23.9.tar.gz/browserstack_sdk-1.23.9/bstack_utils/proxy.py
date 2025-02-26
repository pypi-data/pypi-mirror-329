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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll111l11l_opy_
bstack1ll11lll_opy_ = Config.bstack1l1ll1l1_opy_()
def bstack1ll11llll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll11lll111_opy_(bstack1ll11ll1lll_opy_, bstack1ll11lll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll11ll1lll_opy_):
        with open(bstack1ll11ll1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll11llll11_opy_(bstack1ll11ll1lll_opy_):
        pac = get_pac(url=bstack1ll11ll1lll_opy_)
    else:
        raise Exception(bstack111l1ll_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᚵ").format(bstack1ll11ll1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l1ll_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᚶ"), 80))
        bstack1ll11ll1ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll11ll1ll1_opy_ = bstack111l1ll_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᚷ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll11lll1l1_opy_, bstack1ll11ll1ll1_opy_)
    return proxy_url
def bstack1lll1ll1l1_opy_(config):
    return bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᚸ") in config or bstack111l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᚹ") in config
def bstack1ll1111111_opy_(config):
    if not bstack1lll1ll1l1_opy_(config):
        return
    if config.get(bstack111l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᚺ")):
        return config.get(bstack111l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᚻ"))
    if config.get(bstack111l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᚼ")):
        return config.get(bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᚽ"))
def bstack1111l1l1_opy_(config, bstack1ll11lll1l1_opy_):
    proxy = bstack1ll1111111_opy_(config)
    proxies = {}
    if config.get(bstack111l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᚾ")) or config.get(bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᚿ")):
        if proxy.endswith(bstack111l1ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᛀ")):
            proxies = bstack1111llll1_opy_(proxy, bstack1ll11lll1l1_opy_)
        else:
            proxies = {
                bstack111l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᛁ"): proxy
            }
    bstack1ll11lll_opy_.bstack1l1l11lll1_opy_(bstack111l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᛂ"), proxies)
    return proxies
def bstack1111llll1_opy_(bstack1ll11ll1lll_opy_, bstack1ll11lll1l1_opy_):
    proxies = {}
    global bstack1ll11lll11l_opy_
    if bstack111l1ll_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ᛃ") in globals():
        return bstack1ll11lll11l_opy_
    try:
        proxy = bstack1ll11lll111_opy_(bstack1ll11ll1lll_opy_, bstack1ll11lll1l1_opy_)
        if bstack111l1ll_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦᛄ") in proxy:
            proxies = {}
        elif bstack111l1ll_opy_ (u"ࠧࡎࡔࡕࡒࠥᛅ") in proxy or bstack111l1ll_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᛆ") in proxy or bstack111l1ll_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᛇ") in proxy:
            bstack1ll11lll1ll_opy_ = proxy.split(bstack111l1ll_opy_ (u"ࠣࠢࠥᛈ"))
            if bstack111l1ll_opy_ (u"ࠤ࠽࠳࠴ࠨᛉ") in bstack111l1ll_opy_ (u"ࠥࠦᛊ").join(bstack1ll11lll1ll_opy_[1:]):
                proxies = {
                    bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᛋ"): bstack111l1ll_opy_ (u"ࠧࠨᛌ").join(bstack1ll11lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᛍ"): str(bstack1ll11lll1ll_opy_[0]).lower() + bstack111l1ll_opy_ (u"ࠢ࠻࠱࠲ࠦᛎ") + bstack111l1ll_opy_ (u"ࠣࠤᛏ").join(bstack1ll11lll1ll_opy_[1:])
                }
        elif bstack111l1ll_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᛐ") in proxy:
            bstack1ll11lll1ll_opy_ = proxy.split(bstack111l1ll_opy_ (u"ࠥࠤࠧᛑ"))
            if bstack111l1ll_opy_ (u"ࠦ࠿࠵࠯ࠣᛒ") in bstack111l1ll_opy_ (u"ࠧࠨᛓ").join(bstack1ll11lll1ll_opy_[1:]):
                proxies = {
                    bstack111l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᛔ"): bstack111l1ll_opy_ (u"ࠢࠣᛕ").join(bstack1ll11lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᛖ"): bstack111l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᛗ") + bstack111l1ll_opy_ (u"ࠥࠦᛘ").join(bstack1ll11lll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᛙ"): proxy
            }
    except Exception as e:
        print(bstack111l1ll_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᛚ"), bstack1lll111l11l_opy_.format(bstack1ll11ll1lll_opy_, str(e)))
    bstack1ll11lll11l_opy_ = proxies
    return proxies
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
class bstack1111ll1l11_opy_(object):
  bstack1l11lll1_opy_ = os.path.join(os.path.expanduser(bstack111l1ll_opy_ (u"ࠧࡿࠩၨ")), bstack111l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨၩ"))
  bstack1111l1llll_opy_ = os.path.join(bstack1l11lll1_opy_, bstack111l1ll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩၪ"))
  bstack1111ll11ll_opy_ = None
  perform_scan = None
  bstack1l11111l1_opy_ = None
  bstack1llll1llll_opy_ = None
  bstack111l111111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l1ll_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬၫ")):
      cls.instance = super(bstack1111ll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack1111ll111l_opy_()
    return cls.instance
  def bstack1111ll111l_opy_(self):
    try:
      with open(self.bstack1111l1llll_opy_, bstack111l1ll_opy_ (u"ࠫࡷ࠭ၬ")) as bstack1llll111ll_opy_:
        bstack1111ll11l1_opy_ = bstack1llll111ll_opy_.read()
        data = json.loads(bstack1111ll11l1_opy_)
        if bstack111l1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧၭ") in data:
          self.bstack111l1l1l1l_opy_(data[bstack111l1ll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨၮ")])
        if bstack111l1ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨၯ") in data:
          self.bstack111l1l1111_opy_(data[bstack111l1ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩၰ")])
    except:
      pass
  def bstack111l1l1111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack111l1ll_opy_ (u"ࠩࡶࡧࡦࡴࠧၱ")]
      self.bstack1l11111l1_opy_ = scripts[bstack111l1ll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧၲ")]
      self.bstack1llll1llll_opy_ = scripts[bstack111l1ll_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨၳ")]
      self.bstack111l111111_opy_ = scripts[bstack111l1ll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪၴ")]
  def bstack111l1l1l1l_opy_(self, bstack1111ll11ll_opy_):
    if bstack1111ll11ll_opy_ != None and len(bstack1111ll11ll_opy_) != 0:
      self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def store(self):
    try:
      with open(self.bstack1111l1llll_opy_, bstack111l1ll_opy_ (u"࠭ࡷࠨၵ")) as file:
        json.dump({
          bstack111l1ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤၶ"): self.bstack1111ll11ll_opy_,
          bstack111l1ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤၷ"): {
            bstack111l1ll_opy_ (u"ࠤࡶࡧࡦࡴࠢၸ"): self.perform_scan,
            bstack111l1ll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢၹ"): self.bstack1l11111l1_opy_,
            bstack111l1ll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣၺ"): self.bstack1llll1llll_opy_,
            bstack111l1ll_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥၻ"): self.bstack111l111111_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll1l11l11_opy_(self, bstack1111ll1111_opy_):
    try:
      return any(command.get(bstack111l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫၼ")) == bstack1111ll1111_opy_ for command in self.bstack1111ll11ll_opy_)
    except:
      return False
bstack1l1111l111_opy_ = bstack1111ll1l11_opy_()
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
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lll111l11_opy_, bstack11ll1111_opy_
from bstack_utils.measure import measure
class bstack1llll111_opy_:
  working_dir = os.getcwd()
  bstack1111l1l11_opy_ = False
  config = {}
  binary_path = bstack111l1ll_opy_ (u"ࠬ࠭ᘲ")
  bstack1ll1lllll1l_opy_ = bstack111l1ll_opy_ (u"࠭ࠧᘳ")
  bstack11lllll1_opy_ = False
  bstack1ll1lll1l11_opy_ = None
  bstack1ll1ll1l1ll_opy_ = {}
  bstack1lll1111111_opy_ = 300
  bstack1ll1lllll11_opy_ = False
  logger = None
  bstack1ll1ll1llll_opy_ = False
  bstack1ll1ll1l_opy_ = False
  bstack1l1ll11lll_opy_ = None
  bstack1ll1lllllll_opy_ = bstack111l1ll_opy_ (u"ࠧࠨᘴ")
  bstack1ll1l1l1l11_opy_ = {
    bstack111l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᘵ") : 1,
    bstack111l1ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᘶ") : 2,
    bstack111l1ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᘷ") : 3,
    bstack111l1ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᘸ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1ll1lll1_opy_(self):
    bstack1lll1111l11_opy_ = bstack111l1ll_opy_ (u"ࠬ࠭ᘹ")
    bstack1ll1lll111l_opy_ = sys.platform
    bstack1ll1l1ll111_opy_ = bstack111l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᘺ")
    if re.match(bstack111l1ll_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᘻ"), bstack1ll1lll111l_opy_) != None:
      bstack1lll1111l11_opy_ = bstack11111ll111_opy_ + bstack111l1ll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᘼ")
      self.bstack1ll1lllllll_opy_ = bstack111l1ll_opy_ (u"ࠩࡰࡥࡨ࠭ᘽ")
    elif re.match(bstack111l1ll_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᘾ"), bstack1ll1lll111l_opy_) != None:
      bstack1lll1111l11_opy_ = bstack11111ll111_opy_ + bstack111l1ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᘿ")
      bstack1ll1l1ll111_opy_ = bstack111l1ll_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᙀ")
      self.bstack1ll1lllllll_opy_ = bstack111l1ll_opy_ (u"࠭ࡷࡪࡰࠪᙁ")
    else:
      bstack1lll1111l11_opy_ = bstack11111ll111_opy_ + bstack111l1ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᙂ")
      self.bstack1ll1lllllll_opy_ = bstack111l1ll_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᙃ")
    return bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_
  def bstack1ll1l1ll11l_opy_(self):
    try:
      bstack1ll1l1lll1l_opy_ = [os.path.join(expanduser(bstack111l1ll_opy_ (u"ࠤࢁࠦᙄ")), bstack111l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᙅ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1l1lll1l_opy_:
        if(self.bstack1lll11111l1_opy_(path)):
          return path
      raise bstack111l1ll_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᙆ")
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᙇ").format(e))
  def bstack1lll11111l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  @measure(event_name=EVENTS.bstack111111l1ll_opy_, stage=STAGE.SINGLE)
  def bstack1ll1llll11l_opy_(self, bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_):
    try:
      bstack1ll1ll1ll11_opy_ = self.bstack1ll1l1ll11l_opy_()
      bstack1ll1l1l1l1l_opy_ = os.path.join(bstack1ll1ll1ll11_opy_, bstack111l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᙈ"))
      bstack1ll1ll111ll_opy_ = os.path.join(bstack1ll1ll1ll11_opy_, bstack1ll1l1ll111_opy_)
      if os.path.exists(bstack1ll1ll111ll_opy_):
        self.logger.info(bstack111l1ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᙉ").format(bstack1ll1ll111ll_opy_))
        return bstack1ll1ll111ll_opy_
      if os.path.exists(bstack1ll1l1l1l1l_opy_):
        self.logger.info(bstack111l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᙊ").format(bstack1ll1l1l1l1l_opy_))
        return self.bstack1ll1l1l1lll_opy_(bstack1ll1l1l1l1l_opy_, bstack1ll1l1ll111_opy_)
      self.logger.info(bstack111l1ll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᙋ").format(bstack1lll1111l11_opy_))
      response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠪࡋࡊ࡚ࠧᙌ"), bstack1lll1111l11_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1ll1l1l1l1l_opy_, bstack111l1ll_opy_ (u"ࠫࡼࡨࠧᙍ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l1ll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᙎ").format(bstack1ll1l1l1l1l_opy_))
        return self.bstack1ll1l1l1lll_opy_(bstack1ll1l1l1l1l_opy_, bstack1ll1l1ll111_opy_)
      else:
        raise(bstack111l1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᙏ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᙐ").format(e))
  def bstack1ll1l1ll1l1_opy_(self, bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_):
    try:
      retry = 2
      bstack1ll1ll111ll_opy_ = None
      bstack1ll1lll1111_opy_ = False
      while retry > 0:
        bstack1ll1ll111ll_opy_ = self.bstack1ll1llll11l_opy_(bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_)
        bstack1ll1lll1111_opy_ = self.bstack1ll1llllll1_opy_(bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_, bstack1ll1ll111ll_opy_)
        if bstack1ll1lll1111_opy_:
          break
        retry -= 1
      return bstack1ll1ll111ll_opy_, bstack1ll1lll1111_opy_
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᙑ").format(e))
    return bstack1ll1ll111ll_opy_, False
  def bstack1ll1llllll1_opy_(self, bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_, bstack1ll1ll111ll_opy_, bstack1ll1ll1ll1l_opy_ = 0):
    if bstack1ll1ll1ll1l_opy_ > 1:
      return False
    if bstack1ll1ll111ll_opy_ == None or os.path.exists(bstack1ll1ll111ll_opy_) == False:
      self.logger.warn(bstack111l1ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᙒ"))
      return False
    bstack1ll1ll11l11_opy_ = bstack111l1ll_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᙓ")
    command = bstack111l1ll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᙔ").format(bstack1ll1ll111ll_opy_)
    bstack1ll1lll1ll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1ll1ll11l11_opy_, bstack1ll1lll1ll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᙕ"))
      return False
  def bstack1ll1l1l1lll_opy_(self, bstack1ll1l1l1l1l_opy_, bstack1ll1l1ll111_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1l1l1l1l_opy_)
      shutil.unpack_archive(bstack1ll1l1l1l1l_opy_, working_dir)
      bstack1ll1ll111ll_opy_ = os.path.join(working_dir, bstack1ll1l1ll111_opy_)
      os.chmod(bstack1ll1ll111ll_opy_, 0o755)
      return bstack1ll1ll111ll_opy_
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᙖ"))
  def bstack1ll1lll11ll_opy_(self):
    try:
      bstack1ll1lll1lll_opy_ = self.config.get(bstack111l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᙗ"))
      bstack1ll1lll11ll_opy_ = bstack1ll1lll1lll_opy_ or (bstack1ll1lll1lll_opy_ is None and self.bstack1111l1l11_opy_)
      if not bstack1ll1lll11ll_opy_ or self.config.get(bstack111l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᙘ"), None) not in bstack11111llll1_opy_:
        return False
      self.bstack11lllll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᙙ").format(e))
  def bstack1lll11111ll_opy_(self):
    try:
      bstack1lll11111ll_opy_ = self.bstack1ll1l1l111l_opy_
      return bstack1lll11111ll_opy_
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᙚ").format(e))
  def init(self, bstack1111l1l11_opy_, config, logger):
    self.bstack1111l1l11_opy_ = bstack1111l1l11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1ll1lll11ll_opy_():
      return
    self.bstack1ll1ll1l1ll_opy_ = config.get(bstack111l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᙛ"), {})
    self.bstack1ll1l1l111l_opy_ = config.get(bstack111l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᙜ"))
    try:
      bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_ = self.bstack1ll1ll1lll1_opy_()
      bstack1ll1ll111ll_opy_, bstack1ll1lll1111_opy_ = self.bstack1ll1l1ll1l1_opy_(bstack1lll1111l11_opy_, bstack1ll1l1ll111_opy_)
      if bstack1ll1lll1111_opy_:
        self.binary_path = bstack1ll1ll111ll_opy_
        thread = Thread(target=self.bstack1ll1ll11111_opy_)
        thread.start()
      else:
        self.bstack1ll1ll1llll_opy_ = True
        self.logger.error(bstack111l1ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᙝ").format(bstack1ll1ll111ll_opy_))
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᙞ").format(e))
  def bstack1ll1l1lll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬᙟ"), bstack111l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᙠ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l1ll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᙡ").format(logfile))
      self.bstack1ll1lllll1l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᙢ").format(e))
  @measure(event_name=EVENTS.bstack111111l1l1_opy_, stage=STAGE.SINGLE)
  def bstack1ll1ll11111_opy_(self):
    bstack1ll1ll11l1l_opy_ = self.bstack1ll1llll1ll_opy_()
    if bstack1ll1ll11l1l_opy_ == None:
      self.bstack1ll1ll1llll_opy_ = True
      self.logger.error(bstack111l1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᙣ"))
      return False
    command_args = [bstack111l1ll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᙤ") if self.bstack1111l1l11_opy_ else bstack111l1ll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᙥ")]
    bstack1lll11l111l_opy_ = self.bstack1ll1ll1l11l_opy_()
    if bstack1lll11l111l_opy_ != None:
      command_args.append(bstack111l1ll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᙦ").format(bstack1lll11l111l_opy_))
    env = os.environ.copy()
    env[bstack111l1ll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᙧ")] = bstack1ll1ll11l1l_opy_
    env[bstack111l1ll_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᙨ")] = os.environ.get(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᙩ"), bstack111l1ll_opy_ (u"ࠬ࠭ᙪ"))
    bstack1ll1lll1l1l_opy_ = [self.binary_path]
    self.bstack1ll1l1lll11_opy_()
    self.bstack1ll1lll1l11_opy_ = self.bstack1ll1ll11ll1_opy_(bstack1ll1lll1l1l_opy_ + command_args, env)
    self.logger.debug(bstack111l1ll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᙫ"))
    bstack1ll1ll1ll1l_opy_ = 0
    while self.bstack1ll1lll1l11_opy_.poll() == None:
      bstack1ll1ll11lll_opy_ = self.bstack1ll1l1ll1ll_opy_()
      if bstack1ll1ll11lll_opy_:
        self.logger.debug(bstack111l1ll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᙬ"))
        self.bstack1ll1lllll11_opy_ = True
        return True
      bstack1ll1ll1ll1l_opy_ += 1
      self.logger.debug(bstack111l1ll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦ᙭").format(bstack1ll1ll1ll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack111l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢ᙮").format(bstack1ll1ll1ll1l_opy_))
    self.bstack1ll1ll1llll_opy_ = True
    return False
  def bstack1ll1l1ll1ll_opy_(self, bstack1ll1ll1ll1l_opy_ = 0):
    if bstack1ll1ll1ll1l_opy_ > 10:
      return False
    try:
      bstack1ll1l1l11ll_opy_ = os.environ.get(bstack111l1ll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᙯ"), bstack111l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᙰ"))
      bstack1ll1ll111l1_opy_ = bstack1ll1l1l11ll_opy_ + bstack111111lll1_opy_
      response = requests.get(bstack1ll1ll111l1_opy_)
      data = response.json()
      self.bstack1l1ll11lll_opy_ = data.get(bstack111l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᙱ"), {}).get(bstack111l1ll_opy_ (u"࠭ࡩࡥࠩᙲ"), None)
      return True
    except:
      self.logger.debug(bstack111l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᙳ"))
      return False
  def bstack1ll1llll1ll_opy_(self):
    bstack1ll1ll1l111_opy_ = bstack111l1ll_opy_ (u"ࠨࡣࡳࡴࠬᙴ") if self.bstack1111l1l11_opy_ else bstack111l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᙵ")
    bstack1ll1l1l11l1_opy_ = bstack111l1ll_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᙶ") if self.config.get(bstack111l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᙷ")) is None else True
    bstack1lll1llll1l_opy_ = bstack111l1ll_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨᙸ").format(self.config[bstack111l1ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᙹ")], bstack1ll1ll1l111_opy_, bstack1ll1l1l11l1_opy_)
    if self.bstack1ll1l1l111l_opy_:
      bstack1lll1llll1l_opy_ += bstack111l1ll_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᙺ").format(self.bstack1ll1l1l111l_opy_)
    uri = bstack1lll111l11_opy_(bstack1lll1llll1l_opy_)
    try:
      response = bstack11ll1111_opy_(bstack111l1ll_opy_ (u"ࠨࡉࡈࡘࠬᙻ"), uri, {}, {bstack111l1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᙼ"): (self.config[bstack111l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᙽ")], self.config[bstack111l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᙾ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11lllll1_opy_ = data.get(bstack111l1ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᙿ"))
        self.bstack1ll1l1l111l_opy_ = data.get(bstack111l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫ "))
        os.environ[bstack111l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᚁ")] = str(self.bstack11lllll1_opy_)
        os.environ[bstack111l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᚂ")] = str(self.bstack1ll1l1l111l_opy_)
        if bstack1ll1l1l11l1_opy_ == bstack111l1ll_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᚃ") and str(self.bstack11lllll1_opy_).lower() == bstack111l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᚄ"):
          self.bstack1ll1ll1l_opy_ = True
        if bstack111l1ll_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᚅ") in data:
          return data[bstack111l1ll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᚆ")]
        else:
          raise bstack111l1ll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᚇ").format(data)
      else:
        raise bstack111l1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᚈ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᚉ").format(e))
  def bstack1ll1ll1l11l_opy_(self):
    bstack1ll1ll1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l1ll_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᚊ"))
    try:
      if bstack111l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᚋ") not in self.bstack1ll1ll1l1ll_opy_:
        self.bstack1ll1ll1l1ll_opy_[bstack111l1ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᚌ")] = 2
      with open(bstack1ll1ll1111l_opy_, bstack111l1ll_opy_ (u"ࠬࡽࠧᚍ")) as fp:
        json.dump(self.bstack1ll1ll1l1ll_opy_, fp)
      return bstack1ll1ll1111l_opy_
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᚎ").format(e))
  def bstack1ll1ll11ll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1lllllll_opy_ == bstack111l1ll_opy_ (u"ࠧࡸ࡫ࡱࠫᚏ"):
        bstack1ll1l1l1ll1_opy_ = [bstack111l1ll_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᚐ"), bstack111l1ll_opy_ (u"ࠩ࠲ࡧࠬᚑ")]
        cmd = bstack1ll1l1l1ll1_opy_ + cmd
      cmd = bstack111l1ll_opy_ (u"ࠪࠤࠬᚒ").join(cmd)
      self.logger.debug(bstack111l1ll_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᚓ").format(cmd))
      with open(self.bstack1ll1lllll1l_opy_, bstack111l1ll_opy_ (u"ࠧࡧࠢᚔ")) as bstack1lll111111l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll111111l_opy_, text=True, stderr=bstack1lll111111l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1ll1llll_opy_ = True
      self.logger.error(bstack111l1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᚕ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1ll1lllll11_opy_:
        self.logger.info(bstack111l1ll_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᚖ"))
        cmd = [self.binary_path, bstack111l1ll_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᚗ")]
        self.bstack1ll1ll11ll1_opy_(cmd)
        self.bstack1ll1lllll11_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᚘ").format(cmd, e))
  def bstack1ll1lll11l_opy_(self):
    if not self.bstack11lllll1_opy_:
      return
    try:
      bstack1ll1ll1l1l1_opy_ = 0
      while not self.bstack1ll1lllll11_opy_ and bstack1ll1ll1l1l1_opy_ < self.bstack1lll1111111_opy_:
        if self.bstack1ll1ll1llll_opy_:
          self.logger.info(bstack111l1ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᚙ"))
          return
        time.sleep(1)
        bstack1ll1ll1l1l1_opy_ += 1
      os.environ[bstack111l1ll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᚚ")] = str(self.bstack1ll1l1lllll_opy_())
      self.logger.info(bstack111l1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨ᚛"))
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ᚜").format(e))
  def bstack1ll1l1lllll_opy_(self):
    if self.bstack1111l1l11_opy_:
      return
    try:
      bstack1ll1llll111_opy_ = [platform[bstack111l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᚝")].lower() for platform in self.config.get(bstack111l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᚞"), [])]
      bstack1ll1llll1l1_opy_ = sys.maxsize
      bstack1ll1l1llll1_opy_ = bstack111l1ll_opy_ (u"ࠩࠪ᚟")
      for browser in bstack1ll1llll111_opy_:
        if browser in self.bstack1ll1l1l1l11_opy_:
          bstack1ll1lll11l1_opy_ = self.bstack1ll1l1l1l11_opy_[browser]
        if bstack1ll1lll11l1_opy_ < bstack1ll1llll1l1_opy_:
          bstack1ll1llll1l1_opy_ = bstack1ll1lll11l1_opy_
          bstack1ll1l1llll1_opy_ = browser
      return bstack1ll1l1llll1_opy_
    except Exception as e:
      self.logger.error(bstack111l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᚠ").format(e))
  @classmethod
  def bstack1l1l111ll1_opy_(self):
    return os.getenv(bstack111l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᚡ"), bstack111l1ll_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫᚢ")).lower()
  @classmethod
  def bstack1ll1111l11_opy_(self):
    return os.getenv(bstack111l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᚣ"), bstack111l1ll_opy_ (u"ࠧࠨᚤ"))
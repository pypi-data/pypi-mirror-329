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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l11ll1ll_opy_ import RobotHandler
from bstack_utils.capture import bstack11l1ll1ll1_opy_
from bstack_utils.bstack11l1ll1l1l_opy_ import bstack11l11ll11l_opy_, bstack11l1ll111l_opy_, bstack11l1l111ll_opy_
from bstack_utils.bstack11l1ll11l1_opy_ import bstack11l111ll1_opy_
from bstack_utils.bstack11l1l11l1l_opy_ import bstack1lll1ll111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11llll11l_opy_, bstack1ll111l1l_opy_, Result, \
    bstack11l1111l11_opy_, bstack11l11l1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ຾"): [],
        bstack111l1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ຿"): [],
        bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧເ"): []
    }
    bstack11l11ll1l1_opy_ = []
    bstack111lllllll_opy_ = []
    @staticmethod
    def bstack11l1lll111_opy_(log):
        if not ((isinstance(log[bstack111l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬແ")], list) or (isinstance(log[bstack111l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ໂ")], dict)) and len(log[bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໃ")])>0) or (isinstance(log[bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨໄ")], str) and log[bstack111l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໅")].strip())):
            return
        active = bstack11l111ll1_opy_.bstack11l1l11lll_opy_()
        log = {
            bstack111l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨໆ"): log[bstack111l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ໇")],
            bstack111l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶ່ࠧ"): bstack11l11l1l11_opy_().isoformat() + bstack111l1ll_opy_ (u"ࠬࡠ້ࠧ"),
            bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫໊ࠧ"): log[bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໋")],
        }
        if active:
            if active[bstack111l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭໌")] == bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧໍ"):
                log[bstack111l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ໎")] = active[bstack111l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ໏")]
            elif active[bstack111l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ໐")] == bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࠫ໑"):
                log[bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໒")] = active[bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໓")]
        bstack1lll1ll111_opy_.bstack11lll111l_opy_([log])
    def __init__(self):
        self.messages = bstack11l11l1111_opy_()
        self._11l11111ll_opy_ = None
        self._111lll11l1_opy_ = None
        self._11l1111111_opy_ = OrderedDict()
        self.bstack11l1l11111_opy_ = bstack11l1ll1ll1_opy_(self.bstack11l1lll111_opy_)
    @bstack11l1111l11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l11llll1_opy_()
        if not self._11l1111111_opy_.get(attrs.get(bstack111l1ll_opy_ (u"ࠩ࡬ࡨࠬ໔")), None):
            self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠪ࡭ࡩ࠭໕"))] = {}
        bstack11l1111lll_opy_ = bstack11l1l111ll_opy_(
                bstack111llll11l_opy_=attrs.get(bstack111l1ll_opy_ (u"ࠫ࡮ࡪࠧ໖")),
                name=name,
                bstack11l1l11l11_opy_=bstack1ll111l1l_opy_(),
                file_path=os.path.relpath(attrs[bstack111l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ໗")], start=os.getcwd()) if attrs.get(bstack111l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭໘")) != bstack111l1ll_opy_ (u"ࠧࠨ໙") else bstack111l1ll_opy_ (u"ࠨࠩ໚"),
                framework=bstack111l1ll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ໛")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l1ll_opy_ (u"ࠪ࡭ࡩ࠭ໜ"), None)
        self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠫ࡮ࡪࠧໝ"))][bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໞ")] = bstack11l1111lll_opy_
    @bstack11l1111l11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l111l1ll_opy_()
        self._11l111lll1_opy_(messages)
        for bstack111llll1ll_opy_ in self.bstack11l11ll1l1_opy_:
            bstack111llll1ll_opy_[bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨໟ")][bstack111l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭໠")].extend(self.store[bstack111l1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໡")])
            bstack1lll1ll111_opy_.bstack1ll111lll_opy_(bstack111llll1ll_opy_)
        self.bstack11l11ll1l1_opy_ = []
        self.store[bstack111l1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ໢")] = []
    @bstack11l1111l11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1l11111_opy_.start()
        if not self._11l1111111_opy_.get(attrs.get(bstack111l1ll_opy_ (u"ࠪ࡭ࡩ࠭໣")), None):
            self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠫ࡮ࡪࠧ໤"))] = {}
        driver = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ໥"), None)
        bstack11l1ll1l1l_opy_ = bstack11l1l111ll_opy_(
            bstack111llll11l_opy_=attrs.get(bstack111l1ll_opy_ (u"࠭ࡩࡥࠩ໦")),
            name=name,
            bstack11l1l11l11_opy_=bstack1ll111l1l_opy_(),
            file_path=os.path.relpath(attrs[bstack111l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ໧")], start=os.getcwd()),
            scope=RobotHandler.bstack111ll1llll_opy_(attrs.get(bstack111l1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໨"), None)),
            framework=bstack111l1ll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ໩"),
            tags=attrs[bstack111l1ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ໪")],
            hooks=self.store[bstack111l1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ໫")],
            bstack11l1l1lll1_opy_=bstack1lll1ll111_opy_.bstack11l1l1llll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l1ll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢ໬").format(bstack111l1ll_opy_ (u"ࠨࠠࠣ໭").join(attrs[bstack111l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬ໮")]), name) if attrs[bstack111l1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭໯")] else name
        )
        self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠩ࡬ࡨࠬ໰"))][bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໱")] = bstack11l1ll1l1l_opy_
        threading.current_thread().current_test_uuid = bstack11l1ll1l1l_opy_.bstack11l11ll111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l1ll_opy_ (u"ࠫ࡮ࡪࠧ໲"), None)
        self.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭໳"), bstack11l1ll1l1l_opy_)
    @bstack11l1111l11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1l11111_opy_.reset()
        bstack11l11l11l1_opy_ = bstack111lllll11_opy_.get(attrs.get(bstack111l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭໴")), bstack111l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ໵"))
        self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠨ࡫ࡧࠫ໶"))][bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໷")].stop(time=bstack1ll111l1l_opy_(), duration=int(attrs.get(bstack111l1ll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ໸"), bstack111l1ll_opy_ (u"ࠫ࠵࠭໹"))), result=Result(result=bstack11l11l11l1_opy_, exception=attrs.get(bstack111l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໺")), bstack11l1ll1111_opy_=[attrs.get(bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໻"))]))
        self.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ໼"), self._11l1111111_opy_[attrs.get(bstack111l1ll_opy_ (u"ࠨ࡫ࡧࠫ໽"))][bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໾")], True)
        self.store[bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ໿")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l1111l11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l11llll1_opy_()
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ༀ"), None)
        bstack11l1111ll1_opy_ = current_test_id if bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ༁"), None) else bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ༂"), None)
        if attrs.get(bstack111l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ༃"), bstack111l1ll_opy_ (u"ࠨࠩ༄")).lower() in [bstack111l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ༅"), bstack111l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ༆")]:
            hook_type = bstack111lll1lll_opy_(attrs.get(bstack111l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ༇")), bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ༈"), None))
            hook_name = bstack111l1ll_opy_ (u"࠭ࡻࡾࠩ༉").format(attrs.get(bstack111l1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ༊"), bstack111l1ll_opy_ (u"ࠨࠩ་")))
            if hook_type in [bstack111l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭༌"), bstack111l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭།")]:
                hook_name = bstack111l1ll_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬ༎").format(bstack11l111l11l_opy_.get(hook_type), attrs.get(bstack111l1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ༏"), bstack111l1ll_opy_ (u"࠭ࠧ༐")))
            bstack111lll1l1l_opy_ = bstack11l1ll111l_opy_(
                bstack111llll11l_opy_=bstack11l1111ll1_opy_ + bstack111l1ll_opy_ (u"ࠧ࠮ࠩ༑") + attrs.get(bstack111l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭༒"), bstack111l1ll_opy_ (u"ࠩࠪ༓")).lower(),
                name=hook_name,
                bstack11l1l11l11_opy_=bstack1ll111l1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ༔")), start=os.getcwd()),
                framework=bstack111l1ll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ༕"),
                tags=attrs[bstack111l1ll_opy_ (u"ࠬࡺࡡࡨࡵࠪ༖")],
                scope=RobotHandler.bstack111ll1llll_opy_(attrs.get(bstack111l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭༗"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111lll1l1l_opy_.bstack11l11ll111_opy_()
            threading.current_thread().current_hook_id = bstack11l1111ll1_opy_ + bstack111l1ll_opy_ (u"ࠧ࠮༘ࠩ") + attrs.get(bstack111l1ll_opy_ (u"ࠨࡶࡼࡴࡪ༙࠭"), bstack111l1ll_opy_ (u"ࠩࠪ༚")).lower()
            self.store[bstack111l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༛")] = [bstack111lll1l1l_opy_.bstack11l11ll111_opy_()]
            if bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ༜"), None):
                self.store[bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༝")].append(bstack111lll1l1l_opy_.bstack11l11ll111_opy_())
            else:
                self.store[bstack111l1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༞")].append(bstack111lll1l1l_opy_.bstack11l11ll111_opy_())
            if bstack11l1111ll1_opy_:
                self._11l1111111_opy_[bstack11l1111ll1_opy_ + bstack111l1ll_opy_ (u"ࠧ࠮ࠩ༟") + attrs.get(bstack111l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭༠"), bstack111l1ll_opy_ (u"ࠩࠪ༡")).lower()] = { bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༢"): bstack111lll1l1l_opy_ }
            bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ༣"), bstack111lll1l1l_opy_)
        else:
            bstack11l1l1l1l1_opy_ = {
                bstack111l1ll_opy_ (u"ࠬ࡯ࡤࠨ༤"): uuid4().__str__(),
                bstack111l1ll_opy_ (u"࠭ࡴࡦࡺࡷࠫ༥"): bstack111l1ll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭༦").format(attrs.get(bstack111l1ll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ༧")), attrs.get(bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ༨"), bstack111l1ll_opy_ (u"ࠪࠫ༩"))) if attrs.get(bstack111l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ༪"), []) else attrs.get(bstack111l1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ༫")),
                bstack111l1ll_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭༬"): attrs.get(bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬ༭"), []),
                bstack111l1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ༮"): bstack1ll111l1l_opy_(),
                bstack111l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ༯"): bstack111l1ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ༰"),
                bstack111l1ll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ༱"): attrs.get(bstack111l1ll_opy_ (u"ࠬࡪ࡯ࡤࠩ༲"), bstack111l1ll_opy_ (u"࠭ࠧ༳"))
            }
            if attrs.get(bstack111l1ll_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨ༴"), bstack111l1ll_opy_ (u"ࠨ༵ࠩ")) != bstack111l1ll_opy_ (u"ࠩࠪ༶"):
                bstack11l1l1l1l1_opy_[bstack111l1ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧ༷ࠫ")] = attrs.get(bstack111l1ll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ༸"))
            if not self.bstack111lllllll_opy_:
                self._11l1111111_opy_[self._11l11l111l_opy_()][bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༹")].add_step(bstack11l1l1l1l1_opy_)
                threading.current_thread().current_step_uuid = bstack11l1l1l1l1_opy_[bstack111l1ll_opy_ (u"࠭ࡩࡥࠩ༺")]
            self.bstack111lllllll_opy_.append(bstack11l1l1l1l1_opy_)
    @bstack11l1111l11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l111l1ll_opy_()
        self._11l111lll1_opy_(messages)
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩ༻"), None)
        bstack11l1111ll1_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ༼"), None)
        bstack11l111ll1l_opy_ = bstack111lllll11_opy_.get(attrs.get(bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ༽")), bstack111l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ༾"))
        bstack11l11l11ll_opy_ = attrs.get(bstack111l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༿"))
        if bstack11l111ll1l_opy_ != bstack111l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ཀ") and not attrs.get(bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཁ")) and self._11l11111ll_opy_:
            bstack11l11l11ll_opy_ = self._11l11111ll_opy_
        bstack11l1l1ll1l_opy_ = Result(result=bstack11l111ll1l_opy_, exception=bstack11l11l11ll_opy_, bstack11l1ll1111_opy_=[bstack11l11l11ll_opy_])
        if attrs.get(bstack111l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬག"), bstack111l1ll_opy_ (u"ࠨࠩགྷ")).lower() in [bstack111l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨང"), bstack111l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬཅ")]:
            bstack11l1111ll1_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧཆ"), None)
            if bstack11l1111ll1_opy_:
                bstack11l1lll11l_opy_ = bstack11l1111ll1_opy_ + bstack111l1ll_opy_ (u"ࠧ࠳ࠢཇ") + attrs.get(bstack111l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ཈"), bstack111l1ll_opy_ (u"ࠧࠨཉ")).lower()
                self._11l1111111_opy_[bstack11l1lll11l_opy_][bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫཊ")].stop(time=bstack1ll111l1l_opy_(), duration=int(attrs.get(bstack111l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧཋ"), bstack111l1ll_opy_ (u"ࠪ࠴ࠬཌ"))), result=bstack11l1l1ll1l_opy_)
                bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ཌྷ"), self._11l1111111_opy_[bstack11l1lll11l_opy_][bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཎ")])
        else:
            bstack11l1111ll1_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨཏ"), None)
            if bstack11l1111ll1_opy_ and len(self.bstack111lllllll_opy_) == 1:
                current_step_uuid = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫཐ"), None)
                self._11l1111111_opy_[bstack11l1111ll1_opy_][bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫད")].bstack11l1l1l1ll_opy_(current_step_uuid, duration=int(attrs.get(bstack111l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧདྷ"), bstack111l1ll_opy_ (u"ࠪ࠴ࠬན"))), result=bstack11l1l1ll1l_opy_)
            else:
                self.bstack11l111ll11_opy_(attrs)
            self.bstack111lllllll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l1ll_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩཔ"), bstack111l1ll_opy_ (u"ࠬࡴ࡯ࠨཕ")) == bstack111l1ll_opy_ (u"࠭ࡹࡦࡵࠪབ"):
                return
            self.messages.push(message)
            bstack11l11l1lll_opy_ = []
            if bstack11l111ll1_opy_.bstack11l1l11lll_opy_():
                bstack11l11l1lll_opy_.append({
                    bstack111l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪབྷ"): bstack1ll111l1l_opy_(),
                    bstack111l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩམ"): message.get(bstack111l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཙ")),
                    bstack111l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩཚ"): message.get(bstack111l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪཛ")),
                    **bstack11l111ll1_opy_.bstack11l1l11lll_opy_()
                })
                if len(bstack11l11l1lll_opy_) > 0:
                    bstack1lll1ll111_opy_.bstack11lll111l_opy_(bstack11l11l1lll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lll1ll111_opy_.bstack111lll1l11_opy_()
    def bstack11l111ll11_opy_(self, bstack111lll1ll1_opy_):
        if not bstack11l111ll1_opy_.bstack11l1l11lll_opy_():
            return
        kwname = bstack111l1ll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫཛྷ").format(bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ཝ")), bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬཞ"), bstack111l1ll_opy_ (u"ࠨࠩཟ"))) if bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧའ"), []) else bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪཡ"))
        error_message = bstack111l1ll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥར").format(kwname, bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬལ")), str(bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཤ"))))
        bstack11l111l111_opy_ = bstack111l1ll_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨཥ").format(kwname, bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨས")))
        bstack11l11l1ll1_opy_ = error_message if bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཧ")) else bstack11l111l111_opy_
        bstack11l111l1l1_opy_ = {
            bstack111l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ཨ"): self.bstack111lllllll_opy_[-1].get(bstack111l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨཀྵ"), bstack1ll111l1l_opy_()),
            bstack111l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཪ"): bstack11l11l1ll1_opy_,
            bstack111l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬཫ"): bstack111l1ll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ཬ") if bstack111lll1ll1_opy_.get(bstack111l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ཭")) == bstack111l1ll_opy_ (u"ࠩࡉࡅࡎࡒࠧ཮") else bstack111l1ll_opy_ (u"ࠪࡍࡓࡌࡏࠨ཯"),
            **bstack11l111ll1_opy_.bstack11l1l11lll_opy_()
        }
        bstack1lll1ll111_opy_.bstack11lll111l_opy_([bstack11l111l1l1_opy_])
    def _11l11l111l_opy_(self):
        for bstack111llll11l_opy_ in reversed(self._11l1111111_opy_):
            bstack11l11l1l1l_opy_ = bstack111llll11l_opy_
            data = self._11l1111111_opy_[bstack111llll11l_opy_][bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ཰")]
            if isinstance(data, bstack11l1ll111l_opy_):
                if not bstack111l1ll_opy_ (u"ࠬࡋࡁࡄࡊཱࠪ") in data.bstack111llllll1_opy_():
                    return bstack11l11l1l1l_opy_
            else:
                return bstack11l11l1l1l_opy_
    def _11l111lll1_opy_(self, messages):
        try:
            bstack111lll1111_opy_ = BuiltIn().get_variable_value(bstack111l1ll_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁིࠧ")) in (bstack11l1111l1l_opy_.DEBUG, bstack11l1111l1l_opy_.TRACE)
            for message, bstack11l111llll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱི"))
                level = message.get(bstack111l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲུࠧ"))
                if level == bstack11l1111l1l_opy_.FAIL:
                    self._11l11111ll_opy_ = name or self._11l11111ll_opy_
                    self._111lll11l1_opy_ = bstack11l111llll_opy_.get(bstack111l1ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧཱུࠥ")) if bstack111lll1111_opy_ and bstack11l111llll_opy_ else self._111lll11l1_opy_
        except:
            pass
    @classmethod
    def bstack11l1ll1l11_opy_(self, event: str, bstack11l111111l_opy_: bstack11l11ll11l_opy_, bstack111lll111l_opy_=False):
        if event == bstack111l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬྲྀ"):
            bstack11l111111l_opy_.set(hooks=self.store[bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨཷ")])
        if event == bstack111l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ླྀ"):
            event = bstack111l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨཹ")
        if bstack111lll111l_opy_:
            bstack111lllll1l_opy_ = {
                bstack111l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨེࠫ"): event,
                bstack11l111111l_opy_.bstack11l11lll1l_opy_(): bstack11l111111l_opy_.bstack11l11111l1_opy_(event)
            }
            self.bstack11l11ll1l1_opy_.append(bstack111lllll1l_opy_)
        else:
            bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(event, bstack11l111111l_opy_)
class bstack11l11l1111_opy_:
    def __init__(self):
        self._111lll11ll_opy_ = []
    def bstack11l11llll1_opy_(self):
        self._111lll11ll_opy_.append([])
    def bstack11l111l1ll_opy_(self):
        return self._111lll11ll_opy_.pop() if self._111lll11ll_opy_ else list()
    def push(self, message):
        self._111lll11ll_opy_[-1].append(message) if self._111lll11ll_opy_ else self._111lll11ll_opy_.append([message])
class bstack11l1111l1l_opy_:
    FAIL = bstack111l1ll_opy_ (u"ࠨࡈࡄࡍࡑཻ࠭")
    ERROR = bstack111l1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨོ")
    WARNING = bstack111l1ll_opy_ (u"࡛ࠪࡆࡘࡎࠨཽ")
    bstack11l11lllll_opy_ = bstack111l1ll_opy_ (u"ࠫࡎࡔࡆࡐࠩཾ")
    DEBUG = bstack111l1ll_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫཿ")
    TRACE = bstack111l1ll_opy_ (u"࠭ࡔࡓࡃࡆࡉྀࠬ")
    bstack111llll111_opy_ = [FAIL, ERROR]
def bstack111llll1l1_opy_(bstack11l11lll11_opy_):
    if not bstack11l11lll11_opy_:
        return None
    if bstack11l11lll11_opy_.get(bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣཱྀࠪ"), None):
        return getattr(bstack11l11lll11_opy_[bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྂ")], bstack111l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧྃ"), None)
    return bstack11l11lll11_opy_.get(bstack111l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ྄"), None)
def bstack111lll1lll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ྅"), bstack111l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ྆")]:
        return
    if hook_type.lower() == bstack111l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ྇"):
        if current_test_uuid is None:
            return bstack111l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫྈ")
        else:
            return bstack111l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ྉ")
    elif hook_type.lower() == bstack111l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫྊ"):
        if current_test_uuid is None:
            return bstack111l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ྋ")
        else:
            return bstack111l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨྌ")
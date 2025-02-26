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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1ll1l1l_opy_ import bstack11l1ll111l_opy_, bstack11l1l111ll_opy_
from bstack_utils.bstack11l1ll11l1_opy_ import bstack11l111ll1_opy_
from bstack_utils.helper import bstack11llll11l_opy_, bstack1ll111l1l_opy_, Result
from bstack_utils.bstack11l1l11l1l_opy_ import bstack1lll1ll111_opy_
from bstack_utils.capture import bstack11l1ll1ll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1111l11l_opy_:
    def __init__(self):
        self.bstack11l1l11111_opy_ = bstack11l1ll1ll1_opy_(self.bstack11l1lll111_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1lll111_opy_(log):
        if not (log[bstack111l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๱")] and log[bstack111l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๲")].strip()):
            return
        active = bstack11l111ll1_opy_.bstack11l1l11lll_opy_()
        log = {
            bstack111l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ๳"): log[bstack111l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๴")],
            bstack111l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ๵"): bstack1ll111l1l_opy_(),
            bstack111l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๶"): log[bstack111l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๷")],
        }
        if active:
            if active[bstack111l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭๸")] == bstack111l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ๹"):
                log[bstack111l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ๺")] = active[bstack111l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ๻")]
            elif active[bstack111l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ๼")] == bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࠫ๽"):
                log[bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ๾")] = active[bstack111l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ๿")]
        bstack1lll1ll111_opy_.bstack11lll111l_opy_([log])
    def start_test(self, attrs):
        bstack11l1l1ll11_opy_ = uuid4().__str__()
        self.tests[bstack11l1l1ll11_opy_] = {}
        self.bstack11l1l11111_opy_.start()
        driver = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ຀"), None)
        bstack11l1ll1l1l_opy_ = bstack11l1l111ll_opy_(
            name=attrs.scenario.name,
            uuid=bstack11l1l1ll11_opy_,
            bstack11l1l11l11_opy_=bstack1ll111l1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111l1ll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦກ"),
            framework=bstack111l1ll_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫຂ"),
            scope=[attrs.feature.name],
            bstack11l1l1lll1_opy_=bstack1lll1ll111_opy_.bstack11l1l1llll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11l1l1ll11_opy_][bstack111l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ຃")] = bstack11l1ll1l1l_opy_
        threading.current_thread().current_test_uuid = bstack11l1l1ll11_opy_
        bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧຄ"), bstack11l1ll1l1l_opy_)
    def end_test(self, attrs):
        bstack11l1lll1l1_opy_ = {
            bstack111l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ຅"): attrs.feature.name,
            bstack111l1ll_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨຆ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1ll1l1l_opy_ = self.tests[current_test_uuid][bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬງ")]
        meta = {
            bstack111l1ll_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦຈ"): bstack11l1lll1l1_opy_,
            bstack111l1ll_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥຉ"): bstack11l1ll1l1l_opy_.meta.get(bstack111l1ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫຊ"), []),
            bstack111l1ll_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ຋"): {
                bstack111l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧຌ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1ll1l1l_opy_.bstack11l1l1111l_opy_(meta)
        bstack11l1ll1l1l_opy_.bstack11l1l1l111_opy_(bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ຍ"), []))
        bstack11l1ll11ll_opy_, exception = self._11l1l11ll1_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1ll1111_opy_=[bstack11l1ll11ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຎ")].stop(time=bstack1ll111l1l_opy_(), duration=int(attrs.duration)*1000, result=bstack11l1l1ll1l_opy_)
        bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬຏ"), self.tests[threading.current_thread().current_test_uuid][bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຐ")])
    def bstack111ll1l1_opy_(self, attrs):
        bstack11l1l1l1l1_opy_ = {
            bstack111l1ll_opy_ (u"ࠬ࡯ࡤࠨຑ"): uuid4().__str__(),
            bstack111l1ll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧຒ"): attrs.keyword,
            bstack111l1ll_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧຓ"): [],
            bstack111l1ll_opy_ (u"ࠨࡶࡨࡼࡹ࠭ດ"): attrs.name,
            bstack111l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ຕ"): bstack1ll111l1l_opy_(),
            bstack111l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪຖ"): bstack111l1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬທ"),
            bstack111l1ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪຘ"): bstack111l1ll_opy_ (u"࠭ࠧນ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪບ")].add_step(bstack11l1l1l1l1_opy_)
        threading.current_thread().current_step_uuid = bstack11l1l1l1l1_opy_[bstack111l1ll_opy_ (u"ࠨ࡫ࡧࠫປ")]
    def bstack1l1l11ll11_opy_(self, attrs):
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ຜ"), None)
        current_step_uuid = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧຝ"), None)
        bstack11l1ll11ll_opy_, exception = self._11l1l11ll1_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1ll1111_opy_=[bstack11l1ll11ll_opy_])
        self.tests[current_test_id][bstack111l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧພ")].bstack11l1l1l1ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l1l1ll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11ll111lll_opy_(self, name, attrs):
        try:
            bstack11l1l1l11l_opy_ = uuid4().__str__()
            self.tests[bstack11l1l1l11l_opy_] = {}
            self.bstack11l1l11111_opy_.start()
            scopes = []
            driver = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫຟ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫຠ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1l1l11l_opy_)
            if name in [bstack111l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦມ"), bstack111l1ll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦຢ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥຣ"), bstack111l1ll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥ຤")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111l1ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬລ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1ll111l_opy_(
                name=name,
                uuid=bstack11l1l1l11l_opy_,
                bstack11l1l11l11_opy_=bstack1ll111l1l_opy_(),
                file_path=file_path,
                framework=bstack111l1ll_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧ຦"),
                bstack11l1l1lll1_opy_=bstack1lll1ll111_opy_.bstack11l1l1llll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111l1ll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢວ"),
                hook_type=name
            )
            self.tests[bstack11l1l1l11l_opy_][bstack111l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥຨ")] = hook_data
            current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧຩ"), None)
            if current_test_id:
                hook_data.bstack11l1l111l1_opy_(current_test_id)
            if name == bstack111l1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨສ"):
                threading.current_thread().before_all_hook_uuid = bstack11l1l1l11l_opy_
            threading.current_thread().current_hook_uuid = bstack11l1l1l11l_opy_
            bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦຫ"), hook_data)
        except Exception as e:
            logger.debug(bstack111l1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥຬ"), name, e)
    def bstack1l111l1l1l_opy_(self, attrs):
        bstack11l1lll11l_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩອ"), None)
        hook_data = self.tests[bstack11l1lll11l_opy_][bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຮ")]
        status = bstack111l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢຯ")
        exception = None
        bstack11l1ll11ll_opy_ = None
        if hook_data.name == bstack111l1ll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦະ"):
            self.bstack11l1l11111_opy_.reset()
            bstack11l1ll1lll_opy_ = self.tests[bstack11llll11l_opy_(threading.current_thread(), bstack111l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩັ"), None)][bstack111l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭າ")].result.result
            if bstack11l1ll1lll_opy_ == bstack111l1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦຳ"):
                if attrs.hook_failures == 1:
                    status = bstack111l1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧິ")
                elif attrs.hook_failures == 2:
                    status = bstack111l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨີ")
            elif attrs.bstack11l1lll1ll_opy_:
                status = bstack111l1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢຶ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111l1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬື") and attrs.hook_failures == 1:
                status = bstack111l1ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤຸ")
            elif hasattr(attrs, bstack111l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧູࠪ")) and attrs.error_message:
                status = bstack111l1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧ຺ࠦ")
            bstack11l1ll11ll_opy_, exception = self._11l1l11ll1_opy_(attrs)
        bstack11l1l1ll1l_opy_ = Result(result=status, exception=exception, bstack11l1ll1111_opy_=[bstack11l1ll11ll_opy_])
        hook_data.stop(time=bstack1ll111l1l_opy_(), duration=0, result=bstack11l1l1ll1l_opy_)
        bstack1lll1ll111_opy_.bstack11l1ll1l11_opy_(bstack111l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧົ"), self.tests[bstack11l1lll11l_opy_][bstack111l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຼ")])
        threading.current_thread().current_hook_uuid = None
    def _11l1l11ll1_opy_(self, attrs):
        try:
            import traceback
            bstack1ll1l111l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l1ll11ll_opy_ = bstack1ll1l111l_opy_[-1] if bstack1ll1l111l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦຽ"))
            bstack11l1ll11ll_opy_ = None
            exception = None
        return bstack11l1ll11ll_opy_, exception
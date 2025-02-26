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
import logging
logger = logging.getLogger(__name__)
bstack1ll11l11lll_opy_ = 1000
bstack1ll11l11l11_opy_ = 2
class bstack1ll111lll11_opy_:
    def __init__(self, handler, bstack1ll111lll1l_opy_=bstack1ll11l11lll_opy_, bstack1ll111llll1_opy_=bstack1ll11l11l11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll111lll1l_opy_ = bstack1ll111lll1l_opy_
        self.bstack1ll111llll1_opy_ = bstack1ll111llll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll11l11l1l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll11l11111_opy_()
    def bstack1ll11l11111_opy_(self):
        self.bstack1ll11l11l1l_opy_ = threading.Event()
        def bstack1ll11l111ll_opy_():
            self.bstack1ll11l11l1l_opy_.wait(self.bstack1ll111llll1_opy_)
            if not self.bstack1ll11l11l1l_opy_.is_set():
                self.bstack1ll11l1111l_opy_()
        self.timer = threading.Thread(target=bstack1ll11l111ll_opy_, daemon=True)
        self.timer.start()
    def bstack1ll11l111l1_opy_(self):
        try:
            if self.bstack1ll11l11l1l_opy_ and not self.bstack1ll11l11l1l_opy_.is_set():
                self.bstack1ll11l11l1l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack111l1ll_opy_ (u"ࠨ࡝ࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࡷࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࠬᜎ") + (str(e) or bstack111l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡨࡵ࡮ࡷࡧࡵࡸࡪࡪࠠࡵࡱࠣࡷࡹࡸࡩ࡯ࡩࠥᜏ")))
        finally:
            self.timer = None
    def bstack1ll111lllll_opy_(self):
        if self.timer:
            self.bstack1ll11l111l1_opy_()
        self.bstack1ll11l11111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll111lll1l_opy_:
                threading.Thread(target=self.bstack1ll11l1111l_opy_).start()
    def bstack1ll11l1111l_opy_(self, source = bstack111l1ll_opy_ (u"ࠪࠫᜐ")):
        with self.lock:
            if not self.queue:
                self.bstack1ll111lllll_opy_()
                return
            data = self.queue[:self.bstack1ll111lll1l_opy_]
            del self.queue[:self.bstack1ll111lll1l_opy_]
        self.handler(data)
        if source != bstack111l1ll_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᜑ"):
            self.bstack1ll111lllll_opy_()
    def shutdown(self):
        self.bstack1ll11l111l1_opy_()
        while self.queue:
            self.bstack1ll11l1111l_opy_(source=bstack111l1ll_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᜒ"))
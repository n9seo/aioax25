#!/usr/bin/env python3

import logging
import gc

from nose.tools import eq_, assert_greater, assert_is, \
        assert_is_not, assert_set_equal

from aioax25.aprs.message import APRSMessageHandler, \
        APRSMessageAckFrame, APRSMessageRejFrame, APRSMessageFrame
from aioax25.frame import AX25Address

from ..loop import DummyLoop


class DummyAPRSHandler(object):
    def __init__(self):
        self._loop = DummyLoop()
        self._retransmit_count = 2
        self._retransmit_timeout_base = 5
        self._retransmit_timeout_rand = 5
        self._retransmit_timeout_scale = 1.5
        self.mycall = AX25Address.decode('N0CALL')
        self._next_msgid = 12345

        self.sent = []
        self.finished = []
    
    def _send(self, frame):
        self.sent.append(frame)

    def _on_msg_handler_finish(self, msgid):
        self.finished.append(msgid)


def test_msghandler_enter_state_success():
    """
    Test the message considers 'SUCCESS' an exit state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.SUCCESS)

    # 'done' signal should have been called.
    eq_(len(calls),1)
    call = calls.pop(0)

    assert_set_equal(set(call.keys()), set(['handler', 'state']))
    assert_is(call['handler'], msghandler)
    eq_(call['state'], msghandler.HandlerState.SUCCESS)

def test_msghandler_enter_state_reject():
    """
    Test the message considers 'REJECT' an exit state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.REJECT)

    # 'done' signal should have been called.
    eq_(len(calls),1)
    call = calls.pop(0)

    assert_set_equal(set(call.keys()), set(['handler', 'state']))
    assert_is(call['handler'], msghandler)
    eq_(call['state'], msghandler.HandlerState.REJECT)

def test_msghandler_enter_state_timeout():
    """
    Test the message considers 'TIMEOUT' an exit state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.TIMEOUT)

    # 'done' signal should have been called.
    eq_(len(calls),1)
    call = calls.pop(0)

    assert_set_equal(set(call.keys()), set(['handler', 'state']))
    assert_is(call['handler'], msghandler)
    eq_(call['state'], msghandler.HandlerState.TIMEOUT)

def test_msghandler_enter_state_cancel():
    """
    Test the message considers 'CANCEL' an exit state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.CANCEL)

    # 'done' signal should have been called.
    eq_(len(calls),1)
    call = calls.pop(0)

    assert_set_equal(set(call.keys()), set(['handler', 'state']))
    assert_is(call['handler'], msghandler)
    eq_(call['state'], msghandler.HandlerState.CANCEL)

def test_msghandler_enter_state_reject():
    """
    Test the message considers 'REJECT' an exit state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.REJECT)

    # 'done' signal should have been called.
    eq_(len(calls),1)
    call = calls.pop(0)

    assert_set_equal(set(call.keys()), set(['handler', 'state']))
    assert_is(call['handler'], msghandler)
    eq_(call['state'], msghandler.HandlerState.REJECT)

def test_msghandler_enter_state_send():
    """
    Test the message considers 'SEND' a intermediate state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.SEND)

    # 'done' signal should not have been called.
    eq_(len(calls),0)

    # State should be reflected in the properties
    eq_(msghandler.state, msghandler.HandlerState.SEND)

def test_msghandler_enter_state_retry():
    """
    Test the message considers 'RETRY' a intermediate state.
    """
    calls = []
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))
    msghandler.done.connect(lambda **k : calls.append(k))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Tell it to go to the success state.
    msghandler._enter_state(msghandler.HandlerState.RETRY)

    # 'done' signal should not have been called.
    eq_(len(calls),0)

    # State should be reflected in the properties
    eq_(msghandler.state, msghandler.HandlerState.RETRY)


def test_msghandler_abort_on_no_aprshandler():
    """
    Test the message handler aborts if the parent APRS handler disappears.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Blow away the APRS handler
    del aprshandler

    # Force garbage collection for pypy's sake.
    gc.collect()

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Now fire the _send method
    msghandler._send()

    # We should have stopped here.
    eq_(msghandler.state, msghandler.HandlerState.FAIL)


def test_msghandler_first_send():
    """
    Test the message handler transmits message on first _send call.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Message handler is still in the INIT state
    eq_(msghandler.state, msghandler.HandlerState.INIT)

    # Now fire the _send method
    msghandler._send()

    # The message should now be in the 'SEND' state
    eq_(msghandler.state, msghandler.HandlerState.SEND)

    # There should be a pending time-out recorded
    eq_(len(aprshandler._loop.calls), 1)
    (calltime, callfunc) = aprshandler._loop.calls.pop(0)

    # Should be at least 5 seconds from now, calling _on_timeout
    assert_greater(calltime, aprshandler._loop.time() + 5.0)
    eq_(callfunc, msghandler._on_timeout)

def test_msghandler_subsequent_send():
    """
    Test the message handler re-transmits message on subsequent _send calls.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force handler into SEND state
    msghandler._state = msghandler.HandlerState.SEND

    # Now fire the _send method
    msghandler._send()

    # The message should now be in the 'RETRY' state
    eq_(msghandler.state, msghandler.HandlerState.RETRY)

    # There should be a pending time-out recorded
    eq_(len(aprshandler._loop.calls), 1)
    (calltime, callfunc) = aprshandler._loop.calls.pop(0)

    # Should be at least 5 seconds from now, calling _on_timeout
    assert_greater(calltime, aprshandler._loop.time() + 5.0)
    eq_(callfunc, msghandler._on_timeout)

    # Retransmit counter should have decremented
    eq_(msghandler._retransmit_count, 1)

def test_msghandler_timeout():
    """
    Test the message handler enters TIMEOUT state when retry count exhausted.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force handler into RETRY state
    msghandler._state = msghandler.HandlerState.RETRY

    # Force retransmit count to zero
    msghandler._retransmit_count = 0

    # Now fire the _send method
    msghandler._send()

    # The message should now be in the 'TIMEOUT' state
    eq_(msghandler.state, msghandler.HandlerState.TIMEOUT)

    # There should be no calls pending
    eq_(len(aprshandler._loop.calls), 0)

def test_msghandler_send_invalid_state():
    """
    Test the message handler refuses to send in the wrong state.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force handler into TIMEOUT state
    msghandler._state = msghandler.HandlerState.TIMEOUT

    try:
        # Now fire the _send method
        msghandler._send()
        assert False, 'This should have raised a RuntimeError'
    except RuntimeError as e:
        eq_(str(e), 'Incorrect state HandlerState.TIMEOUT')

    # There should be no calls pending
    eq_(len(aprshandler._loop.calls), 0)

def test_msghandler_cancel():
    """
    Test calling cancel stops the timer and enters the CANCEL state.
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Inject a dummy time-out object
    timeout = aprshandler._loop.call_later(1.0, None)
    msghandler._retransmit_timeout = timeout

    # Cancel the message
    msghandler.cancel()

    # Handler should now be in the CANCEL state
    eq_(msghandler.state, msghandler.HandlerState.CANCEL)

    # Our time-out should have been cancelled
    eq_(timeout.cancelled(), True)

    # We should no longer be referencing the time-out
    eq_(msghandler._retransmit_timeout, None)

def test_on_timeout():
    """
    Test calling _on_timeout triggers _send
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    msghandler._on_timeout()

    # There should be a pending _send recorded
    eq_(len(aprshandler._loop.calls), 1)
    (calltime, callfunc) = aprshandler._loop.calls.pop(0)

    # Should be pretty much now, calling _send
    assert_greater(calltime, aprshandler._loop.time() - 0.01)
    eq_(callfunc, msghandler._send)

def test_on_response_timedout():
    """
    Test calling _on_response when in TIMEOUT ignores message
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force state, suppose we already received a reply, and a well-meaning
    # digi has repeated it.
    msghandler._state = msghandler.HandlerState.SUCCESS
    frame1 = APRSMessageAckFrame(
            destination='APZAIO',
            source='VK4MSL-9',
            addressee='N0CALL',
            msgid='123'
    )
    msghandler._response = frame1

    frame2 = APRSMessageAckFrame(
                destination='APZAIO',
                source='VK4MSL-9',
                addressee='N0CALL',
                msgid='123'
            )
    msghandler._on_response(frame2)

    # Our official response should be the first one
    assert_is(msghandler.response, frame1)
    assert_is_not(msghandler.response, frame2)

def test_on_response_ack():
    """
    Test calling _on_response with ACK when in SEND triggers SUCCESS
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force state, suppose we just sent our request.
    msghandler._state = msghandler.HandlerState.SEND

    # Pass in our frame
    frame = APRSMessageAckFrame(
            destination='APZAIO',
            source='VK4MSL-9',
            addressee='N0CALL',
            msgid='123'
    )
    msghandler._on_response(frame)

    # Our official response should be the frame we just received
    assert_is(msghandler.response, frame)

    # And we should be done
    eq_(msghandler.state, msghandler.HandlerState.SUCCESS)

def test_on_response_rej():
    """
    Test calling _on_response with REJ when in SEND triggers REJECT
    """
    aprshandler = DummyAPRSHandler()
    msghandler  = APRSMessageHandler(
            aprshandler=aprshandler,
            addressee='CQ',
            path=['WIDE1-1','WIDE2-1'],
            message='testing',
            log=logging.getLogger('messagehandler'))

    # Force state, suppose we just sent our request.
    msghandler._state = msghandler.HandlerState.SEND

    # Pass in our frame
    frame = APRSMessageRejFrame(
            destination='APZAIO',
            source='VK4MSL-9',
            addressee='N0CALL',
            msgid='123'
    )
    msghandler._on_response(frame)

    # Our official response should be the frame we just received
    assert_is(msghandler.response, frame)

    # And we should be done
    eq_(msghandler.state, msghandler.HandlerState.REJECT)
import logging
import functools
import xml.sax

from model_mapper import ModelMapper


logger = logging.getLogger(__package__)


class CallBackHandler(xml.sax.ContentHandler):
    """
        Populate context on behalf of given entities and run callbacks for grabbed instances.
    """
    def __init__(self, cb_map):
        self.cb_map = cb_map
        self.context_stack = None
        self.pending_text = None

    @property
    def is_idle(self):
        return self.context_stack is None

    def startElement(self, name, attrs):
        if name in self.cb_map:
            if not self.is_idle:
                raise RuntimeError('Nested %s' % name)

            self.context_stack = []

        if not self.is_idle:
            self.context_stack.append(
                dict(map(
                    lambda (k, v): ('@%s' % k, v),
                    attrs.items()
                ))
            )

    def characters(self, content):
        if self.pending_text is None:
            self.pending_text = content
        else:
            self.pending_text += content

    def endElement(self, name):
        if not self.is_idle:
            curr_context = self.context_stack.pop()

            if len(curr_context) == 0:
                curr_context = self.pending_text.strip()

            if self.context_stack:
                apply_to = self.context_stack[-1]
                if isinstance(apply_to, dict) and name in apply_to:
                    # it's a list!
                    self.context_stack[-1] = apply_to = [apply_to[name]]

                if isinstance(apply_to, dict):
                    apply_to[name] = curr_context
                else:
                    apply_to.append(curr_context)

            else:
                cb = self.cb_map[name]

                try:
                    cb(curr_context)
                except Exception as e:
                    logger.exception(e)

                self.context_stack = None

        self.pending_text = None


class AbstractCallBackParser(object):
    """
        Looking for entities in the stream
    """
    def __init__(self):
        self.cb_map = {}

    def register_cb(self, name, cb):
        self.cb_map[name] = cb

    def run(self):
        raise NotImplementedError()


class CallBackXMLParser(AbstractCallBackParser):
    def run(self, source):
        xml.sax.parse(source, CallBackHandler(self.cb_map))

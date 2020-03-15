from time import time, sleep
from thingset.packet import SingleFrame

class CSVParser(object):
    def __init__(self, file):
        self.csv = open(file, 'r')
        self.header = next(self.csv).split(';')

    def __iter__(self):
        for line in self.csv:
            content = line.split(';')

            data = bytes.fromhex(''.join([self._make_hex(b) for b in content[4:]]))
            pkt = SingleFrame(data=data)
            identifier = int(content[2], 16) + (0b11 << 24)
            pkt.parseIdentifier(identifier)
            pkt.timestamp = float(content[0])
            yield pkt

        self.csv.close()

    @staticmethod
    def _make_hex(self, string):
        string = string.rstrip()
        if len(string) == 1:
            return '0' + string
        return string

def playback(trace_file, duration=600):
    p = CSVParser(trace_file)
    message = iter(p)
    playback_start = time()
    while (time() - playback_start) < duration:
        pkt = next(message)
        time_diff = time() - playback_start
        if pkt.timestamp * 0.001 <= time_diff:
            print_nice(pkt)
        else:
            sleep(pkt.timestamp * 0.001)
            print_nice(pkt)


def print_nice(msg):
    print("[{}] Prio {} from Source {}: DataObjectID: {} -> {:.3f}".format(msg.timestamp, msg.priority, msg.source,
                                                                           msg.dataobjectID, msg.cbor))

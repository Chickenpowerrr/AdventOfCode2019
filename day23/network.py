import os
import sys
import time
import traceback
from concurrent.futures import as_completed, Future
from concurrent.futures.thread import ThreadPoolExecutor

from day23.input import INSTRUCTIONS
from intcode.computer import Computer


class PacketBuilder:

    def __init__(self, source):
        self.source = source
        self.destination = None
        self.x = None
        self.y = None

    def handle_output(self, value):
        if self.destination is None:
            self.destination = value
        elif self.x is None:
            self.x = value
        else:
            self.y = value

    def finished(self):
        return self.destination is not None and self.x is not None and self.y is not None

    def serialize(self):
        return [self.source, self.destination, self.x, self.y]


class Router:

    waiting = set()

    def __init__(self, address: int):
        self.address = address
        self.queue = []
        self.next_packet = PacketBuilder(address)
        self.connected = None
        self.isp = None
        self.sent_address = False

    def connect(self, computer: Computer):
        self.connected = computer

    def connect_with(self, isp: 'ISP'):
        self.isp = isp

    def send_packet(self, serialized_packet: [int]):
        self.isp.send_packet(serialized_packet)

    def queue_packet(self, serialized_packet: [int]):
        if self.address in self.waiting:
            self.waiting.remove(self.address)

        source = serialized_packet.pop(0)
        target = serialized_packet.pop(0)
        if target == self.address:
            self.queue.append(serialized_packet)
        else:
            print(f'ERROR: invalid packet received from {source}')
            sys.exit()

    def handle_input(self) -> int:
        if self.sent_address:
            if len(self.queue) > 0:
                if self.address in self.waiting:
                    self.waiting.remove(self.address)

                target = self.queue[0]
                value = target.pop(0)
                if len(target) == 0:
                    del self.queue[0]
                return value
            else:
                if self.address not in self.waiting:
                    self.waiting.add(self.address)
                    self.isp.check_idle()
                return -1
        else:
            self.sent_address = True
            return self.address

    def handle_output(self, value: int):
        self.next_packet.handle_output(value)
        if self.next_packet.finished():
            serialized_packet = self.next_packet.serialize()
            self.next_packet = PacketBuilder(self.address)
            self.isp.send_packet(serialized_packet)


class ISP:

    def __init__(self, routers: {int: Router}, nat_enabled=False):
        self.routers = routers
        self.nat_enabled = nat_enabled
        self.nat_previous = [255, 0, -1, -1]
        self.nat_send = False
        self.running = True

        for address in self.routers:
            routers[address].connect_with(self)

    def check_idle(self):
        if self.nat_enabled:
            if sum([len(self.routers[address].queue) for address in self.routers]) == 0:
                if len(Router.waiting) == 50:
                    if not self.nat_send:
                        print('ERROR :(')
                        os._exit(5)

                    self.nat_send = False
                    self.send_packet(self.nat_previous.copy())

    def send_packet(self, serialized_packet: [int]):
        if serialized_packet[1] != 255:
            if self.running:
                print(f'{serialized_packet[0]} -> {serialized_packet[1]}: '
                      f'X={serialized_packet[2]} Y={serialized_packet[3]}')
            self.routers[serialized_packet[1]].queue_packet(serialized_packet)
        else:
            y = serialized_packet[3]

            if not self.nat_enabled:
                print(f'Value at NAT: {y}')
            else:
                print(f'Previous value: {self.nat_previous}')

                if y != self.nat_previous[3]:
                    self.nat_previous = [255, 0, serialized_packet[2], y]
                    if not self.nat_send:
                        self.nat_send = True
                else:
                    self.running = False
                    print(f'{y} occurred twice in at row at the NAT')
                    os._exit(10)


def handle_connect(router: Router, instructions):
    computer = Computer(instructions.copy(), router.handle_input, router.handle_output)
    router.connect(computer)
    computer.execute()


def part1():
    instructions = INSTRUCTIONS
    routers = {address: Router(address) for address in range(50)}
    ISP(routers)

    with ThreadPoolExecutor() as executor:
        [executor.submit(handle_connect, routers[address], instructions)
         for address in range(len(routers))]


def print_length(isp):
    while True:
        time.sleep(10)
        print(f'Found: {[f"{address}: {isp.routers[address].queue}" for address in isp.routers]}')


def part2():
    instructions = INSTRUCTIONS
    routers = {address: Router(address) for address in range(50)}
    isp = ISP(routers, True)

    with ThreadPoolExecutor() as executor:
        connections = [executor.submit(handle_connect, routers[address], instructions)
                       for address in range(len(routers))]

        for f in as_completed(connections):
            exception = f.exception()
            print(exception)
            print('\n'.join(traceback.format_tb(exception.__traceback__)))
            os._exit(1)


if __name__ == '__main__':
    # part1()
    part2()

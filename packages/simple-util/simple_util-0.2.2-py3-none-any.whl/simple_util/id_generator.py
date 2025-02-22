import time
from util import SUtil
class SnowflakeIDGenerator:
    def __init__(self, datacenter_id=1):
        self.machine_id = SUtil.get_machine_id()
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1

        # Bits allocation
        self.machine_id_bits = 5
        self.datacenter_id_bits = 5
        self.sequence_bits = 12

        # Max values
        self.max_machine_id = -1 ^ (-1 << self.machine_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

        # Shifts
        self.machine_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.machine_id_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits + self.datacenter_id_bits

        if self.machine_id > self.max_machine_id or self.machine_id < 0:
            raise ValueError("Machine ID must be between 0 and {}".format(self.max_machine_id))
        if self.datacenter_id > self.max_datacenter_id or self.datacenter_id < 0:
            raise ValueError("Datacenter ID must be between 0 and {}".format(self.max_datacenter_id))

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_for_next_millisecond(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self):
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate ID.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:
                timestamp = self._wait_for_next_millisecond(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return ((timestamp << self.timestamp_shift) |
                (self.datacenter_id << self.datacenter_id_shift) |
                (self.machine_id << self.machine_id_shift) |
                self.sequence)

# Example usage
if __name__ == "__main__":
    id_generator = SnowflakeIDGenerator(datacenter_id=1)
    print(id_generator.generate_id())
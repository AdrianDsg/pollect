import time
from typing import Optional

from fritzconnection import FritzConnection

from pollect.core.ValueSet import ValueSet, Value
from pollect.sources.Source import Source


class FritzSource(Source):
    """
    FritzBox API interaction
    """

    def __init__(self, config):
        super().__init__(config)
        self._pass = config.get('pass')
        self._address = config.get('ip')

        self._last_time = None
        """
        Timestamp of the last run
        
        :type _last_time: float
        """

        self._stats = {}
        """
        Last statistics probed
        
        :type _stats: dict(str, int)
        """

    def _probe(self) -> Optional[ValueSet]:
        connection = FritzConnection(address=self._address, password=self._pass)
        new_data = {}
        output = connection.call_action('WANCommonInterfaceConfig:1', 'GetTotalBytesReceived')
        new_data['recv_bytes_sec'] = output['NewTotalBytesReceived']

        output = connection.call_action('WANCommonInterfaceConfig:1', 'GetTotalBytesSent')
        new_data['sent_bytes_sec'] = output['NewTotalBytesSent']

        data = ValueSet()
        for key, value in new_data.items():
            last_stats = self._stats.get(key)
            self._stats[key] = value
            if last_stats is not None:
                time_delta = int(time.time() - self._last_time)
                data.add(Value(max(0, (value - last_stats) / time_delta), name=key))

        self._last_time = time.time()
        return data

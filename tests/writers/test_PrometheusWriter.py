from unittest import TestCase

import requests

from pollect.core.ValueSet import ValueSet, Value

from pollect.writers.PrometheusWriter import PrometheusWriter


class TestPrometheusWriter(TestCase):
    writer = None

    @staticmethod
    def setUpClass() -> None:
        # Singleton
        if TestPrometheusWriter.writer is None:
            TestPrometheusWriter.writer = PrometheusWriter({'port': 9123})
            TestPrometheusWriter.writer.start()

    def test_removal(self):
        value_set = ValueSet()
        value_set.values.append(Value(0, name='test'))
        self.writer.write([value_set])

        reply = requests.get('http://localhost:9123')
        self.assertIn('test 0.0', reply.text)

        self.writer.write([])
        reply = requests.get('http://localhost:9123')
        self.assertNotIn('test 0.0', reply.text)

        # And add again
        self.writer.write([value_set])
        reply = requests.get('http://localhost:9123')
        self.assertIn('test 0.0', reply.text)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for iSmartAlarm on Android plugin."""

from __future__ import unicode_literals

import unittest

from plaso.lib import definitions
from plaso.parsers.sqlite_plugins import ismartalarm_android

from tests import test_lib as shared_test_lib
from tests.parsers.sqlite_plugins import test_lib


class ISmartAlarmAndroidTest(test_lib.SQLitePluginTestCase):
  """Tests for iSmartAlarm on Android database plugin."""

  @shared_test_lib.skipUnlessHasTestFile(['iSmartAlarm.DB'])
  def testProcess(self):
    """Test the Process function on a iSmartAlarm Android file."""
    plugin = ismartalarm_android.ISmartAlarmAndroidPlugin()
    storage_writer = self._ParseDatabaseFileWithPlugin(
        ['iSmartAlarm.DB'], plugin)

    # We should have 81 events in total.
    self.assertEqual(81, storage_writer.number_of_events)

    events = list(storage_writer.GetSortedEvents())

    # Test IPU event data with action field
    event = events[7]
    self.CheckTimestamp(event.timestamp, '2018-05-15 09:34:20.000000')
    self.assertEqual(
        event.timestamp_desc, definitions.TIME_DESCRIPTION_CREATION)

    self.assertEqual(event.action, '1')
    self.assertEqual(event.ipu_id, '004D3209D9E4')
    self.assertEqual(event.operator, '')
    self.assertEqual(event.profile_id, '')
    self.assertEqual(event.profile_name, '')

    expected_message = ('Action: 1 IPU ID: 004D3209D9E4')
    expected_short_message = ('Action: 1 IPU: 004D3209D9E4')
    self._TestGetMessageStrings(event, expected_message, expected_short_message)

    # Test IPU event data with profile fields
    event = events[10]
    self.CheckTimestamp(event.timestamp, '2018-05-15 12:38:20.000000')
    self.assertEqual(
        event.timestamp_desc, definitions.TIME_DESCRIPTION_CREATION)

    self.assertEqual(event.action, '')
    self.assertEqual(event.ipu_id, '004D3209D9E4')
    self.assertEqual(event.operator, 'JPinkman')
    self.assertEqual(event.profile_id, '0')
    self.assertEqual(event.profile_name, 'ARM')

    expected_message = ('IPU ID: 004D3209D9E4 Operator Name: JPinkman Profile ID: 0 Profile Name: ARM')
    expected_short_message = ('IPU: 004D3209D9E4 Operator Name: JPinkman Profile ID: 0')
    self._TestGetMessageStrings(event, expected_message, expected_short_message)

    # Test sensor event data with no name
    event = events[0]
    self.CheckTimestamp(event.timestamp, '2018-05-14 09:32:45.792000')
    self.assertEqual(
        event.timestamp_desc, definitions.TIME_DESCRIPTION_CREATION)

    self.assertEqual(event.sensor_id, '0006B4E5')
    self.assertEqual(event.action, '6')
    self.assertEqual(event.operator, '004D3209D9E4')
    self.assertEqual(event.name, '')

    expected_message = ('Sensor ID: 0006B4E5 Action: 6 Operator ID: 004D3209D9E4')
    expected_short_message = ('Sensor ID: 0006B4E5 Action: 6 Operator ID: 004D3209D9E4')
    self._TestGetMessageStrings(event, expected_message, expected_short_message)

    # Test sensor event data with name
    event = events[18]
    self.CheckTimestamp(event.timestamp, '2018-05-15 13:03:47.000000')
    self.assertEqual(
        event.timestamp_desc, definitions.TIME_DESCRIPTION_CREATION)

    self.assertEqual(event.sensor_id, '004D3209D9E4')
    self.assertEqual(event.action, '2')
    self.assertEqual(event.operator, '700911')
    self.assertEqual(event.name, 'TheBoss')

    expected_message = ('Sensor ID: 004D3209D9E4 Action: 2 Operator ID: 700911 Operator Name: TheBoss')
    expected_short_message = ('Sensor ID: 004D3209D9E4 Action: 2 Operator ID: 700911')
    self._TestGetMessageStrings(event, expected_message, expected_short_message)

    # Test user event
    event = events[19]
    self.CheckTimestamp(event.timestamp, '2018-05-15 13:03:47.000000')
    self.assertEqual(
        event.timestamp_desc, definitions.TIME_DESCRIPTION_CREATION)

    self.assertEqual(event.id, '700911')
    self.assertEqual(event.action, '4')

    expected_message = ('Operator ID: 700911 Action: 4')
    expected_short_message = ('Operator ID: 700911 Action: 4')
    self._TestGetMessageStrings(event, expected_message, expected_short_message)


if __name__ == '__main__':
  unittest.main()

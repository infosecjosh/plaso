#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for iSmartAlarm on Android database event formatter."""

from __future__ import unicode_literals

import unittest

from plaso.formatters import ismartalarm_android
from tests.formatters import test_lib


class ISmartAlarmAndroidIpuFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the iSmartAlarm on Android contact event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidIpuFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidIpuFormatter()

    expected_attribute_names = [
      'action',
      'ipu_id',
      'operator',
      'profile_id',
      'profile_name'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ISmartAlarmAndroidSensorFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the iSmartAlarm on Android status event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidSensorFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidSensorFormatter()

    expected_attribute_names = [
      'sensor_id',
      'action',
      'operator',
      'name'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ISmartAlarmAndroidUserFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the iSmartAlarm on Android search event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidUserFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = ismartalarm_android.ISmartAlarmAndroidUserFormatter()

    expected_attribute_names = [
      'id',
      'action'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()

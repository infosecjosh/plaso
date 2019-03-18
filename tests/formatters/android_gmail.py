#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Android /userdata/data/com.google.android.gm/databases
/mailstore.username@gmail.com database event formatter."""

from __future__ import unicode_literals

import unittest

from plaso.formatters import android_sms

from tests.formatters import test_lib


class AndroidGmailFormatterTest(test_lib.EventFormatterTestCase):
  """Tests for the Android Gmail event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = android_sms.GmailMessagesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = android_sms.GmailMessagesFormatter()

    expected_attribute_names = [
        'fromAddress', 'to', 'cc', 'bcc', 'ReplyToAddress', 'Subject', 'Snippet', 'Body']

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()

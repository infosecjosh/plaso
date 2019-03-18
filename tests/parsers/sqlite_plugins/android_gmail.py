#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Android Gmail plugin."""

from __future__ import unicode_literals

import unittest

from plaso.formatters import android_gmail as _  # pylint: disable=unused-import
from plaso.lib import definitions
from plaso.parsers.sqlite_plugins import android_gmail

from tests import test_lib as shared_test_lib
from tests.parsers.sqlite_plugins import test_lib


class AndroidGmailTest(test_lib.SQLitePluginTestCase):
  """Tests for the Android Gmail database plugin."""

  @shared_test_lib.skipUnlessHasTestFile(['mailstore.jpinkman2018@gmail.com.db'])
  def testProcess(self):
    """Test the Process function on an Android Gmail Messages mailstore.db file."""
    plugin = android_gmail.GmailMessagePlugin()
    storage_writer = self._ParseDatabaseFileWithPlugin(['mailstore.jpinkman2018@gmail.com.db'], plugin)

    self.assertEqual(storage_writer.number_of_errors, 0)
    self.assertEqual(storage_writer.number_of_events, 40)

    events = list(storage_writer.GetEvents())

    event = events[0]
    self.CheckTimestamp(event.timestamp, '2018-05-15 10:52:05.000000')
    self.assertEqual(event.fromAddress, ('"Samsung account" <SA.noreply@samsung-mail.com>').encode("utf-8"))
    self.assertEqual(event.to, '"JessiePinkman" <jpinkman2018@gmail.com>')
    self.assertEqual(event.snippet, 'Samsung account Benvenuti nei servizi Samsung. Gentile cliente, Il tuo accoun...')


if __name__ == '__main__':
  unittest.main()

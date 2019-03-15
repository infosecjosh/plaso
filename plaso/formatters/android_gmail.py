# -*- coding: utf-8 -*-
"""The Google Gmail messages database event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class GmailMessagesFormatter(interface.ConditionalEventFormatter):
  """Formatter for an Gmail message event."""

  DATA_TYPE = 'android:messaging:gmail'

  FORMAT_STRING_PIECES = [
      'From: {fromAddress}',
      'To: {to}',
      'Cc: {cc}',
      'Bcc: {bcc}',
      'ReplyToAddress: {replyToAddresses}',
      'Subject: {subject}',
      'Snippet: {snippet}',
      'Body: {body}',]

  FORMAT_STRING_SHORT_PIECES = ['{body}']

  SOURCE_LONG = 'Android Google Gmail Message'
  SOURCE_SHORT = 'GMAIL'

manager.FormattersManager.RegisterFormatter(GmailMessagesFormatter)

# -*- coding: utf-8 -*-
"""The Google Gmail messages database event formatter."""

from __future__ import unicode_literals

import pprint
from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors

class GmailMessageFormatter(interface.ConditionalEventFormatter):
  """Formatter for an Gmail message event."""
  DATA_TYPE = 'android:messaging:gmail'

  FORMAT_STRING_PIECES = [
      'From: {fromAddress}',
      'To: {to}',
      'Cc: {cc}',
      'Bcc: {bcc}',
      'ReplyToAddresses: {replyToAddresses}',
      'Subject: {subject}',
      'Snippet: {snippet}',
      'Body: {body}']

  FORMAT_STRING_SHORT_PIECES = ['{body}']

  SOURCE_LONG = 'Android Google Gmail Message'
  SOURCE_SHORT = 'GMAIL'

  def GetMessages(self, unused_formatter_mediator, event):
    """Determines the formatted message strings for an event object.

    If any event values have a matching formatting function in VALUE_FORMATTERS,
    they are run through that function; then the dictionary is passed to the
    superclass's formatting method.

    Args:
      unused_formatter_mediator (FormatterMediator): not used.
      event (EventObject): event.

    Returns:
      tuple(str, str): formatted message string and short message string.

    Raises:
      WrongFormatter: if the event object cannot be formatted by the formatter.
    """
    if self.DATA_TYPE != event.data_type:
      raise errors.WrongFormatter(
          'Unsupported data type: {0:s}.'.format(event.data_type))

    event_values = event.CopyToDict()

    return self._ConditionalFormatMessages(event_values)


manager.FormattersManager.RegisterFormatter(GmailMessageFormatter)

# -*- coding: utf-8 -*-
"""iSmartAlarm on android database formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class ISmartAlarmAndroidIpuFormatter(interface.ConditionalEventFormatter):
  """iSmartAlarm for android IPU event formatter."""

  DATA_TYPE = 'ismartalarm:android:ipuevent'

  FORMAT_STRING_PIECES = [
      'Action: {action}',
      'IPU ID: {ipu_id}',
      'Operator Name: {operator}',
      'Profile ID: {profile_id}',
      'Profile Name: {profile_name}'
  ]

  FORMAT_STRING_SHORT_PIECES = [
      'Action: {action}',
      'IPU: {ipu_id}',
      'Operator Name: {operator}',
      'Profile ID: {profile_id}',
  ]

  SOURCE_LONG = 'iSmartAlarm Android IPU Event'
  SOURCE_SHORT = 'iSmartAlarm Android'


class ISmartAlarmAndroidSensorFormatter(interface.ConditionalEventFormatter):
  """iSmartAlarm for android sensor event formatter."""

  DATA_TYPE = 'ismartalarm:android:sensorevent'

  FORMAT_STRING_PIECES = [
      'Sensor ID: {sensor_id}',
      'Action: {action}',
      'Operator ID: {operator}',
      'Operator Name: {name}'
  ]

  FORMAT_STRING_SHORT_PIECES = [
      'Sensor ID: {sensor_id}',
      'Action: {action}',
      'Operator ID: {operator}'
  ]

  SOURCE_LONG = 'iSmartAlarm Android Sensor Event'
  SOURCE_SHORT = 'iSmartAlarm Android'

  # pylint: disable=unused-argument
  def GetMessages(self, formatter_mediator, event):
    """Determines the formatted message strings for an event object.

    Args:
      formatter_mediator (FormatterMediator): mediates the interactions between
          formatters and other components, such as storage and Windows EventLog
          resources.
      event (EventObject): event.

    Returns:
      tuple(str, str): formatted message string and short message string.

    Raises:
      WrongFormatter: if the event object cannot be formatted by the formatter.
    """
    if self.DATA_TYPE != event.data_type:
      raise errors.WrongFormatter('Unsupported data type: {0:s}.'.format(
          event.data_type))

    event_values = event.CopyToDict()

    # TODO: Map action numbers to descriptive strings here.

    return self._ConditionalFormatMessages(event_values)


class ISmartAlarmAndroidUserFormatter(interface.ConditionalEventFormatter):
  """iSmartAlarm for android user event formatter."""

  DATA_TYPE = 'ismartalarm:android:userevent'

  FORMAT_STRING_PIECES = [
      'Operator ID: {id}',
      'Action: {action}'
  ]

  FORMAT_STRING_SHORT_PIECES = [
      'Operator ID: {id}',
      'Action: {action}'
  ]

  SOURCE_LONG = 'iSmartAlarm Android User Event'
  SOURCE_SHORT = 'iSmartAlarm Android'


manager.FormattersManager.RegisterFormatters([
    ISmartAlarmAndroidIpuFormatter, ISmartAlarmAndroidSensorFormatter,
    ISmartAlarmAndroidUserFormatter])

# -*- coding:utf-8 -*-
"""Parser for iSmartAlarm on Android."""

from __future__ import unicode_literals

from dfdatetime import java_time as dfdatetime_java_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface
from plaso.parsers import logger

class ISmartAlarmAndroidIpuData(events.EventData):
  """ISmartAlarm on Android IPU data.

  Attributes:
    action (int): sensor action identifier.
    ipu_id (int): operator identifier.
    operator (str): operator username
    profile_id (int): system profile identifier.
    profile_name (str): human-readable profile name.
  """

  DATA_TYPE = 'ismartalarm:android:sensorevent'

  def __init__(self):
    """Initializes event data."""
    super(ISmartAlarmAndroidIpuData,
          self).__init__(data_type=self.DATA_TYPE)
    self.action = None
    self.ipu_id = None
    self.operator = None
    self.profile_id = None
    self.profile_name = None


class ISmartAlarmAndroidSensorData(events.EventData):
  """ISmartAlarm on Android sensor data.

  Attributes:
    sensor_id (int): sensor identifier.
    action (int): sensor action identifier.
    operator (int): operator identifier.
    name (str): operator username.
  """

  DATA_TYPE = 'ismartalarm:android:sensorevent'

  def __init__(self):
    """Initializes event data."""
    super(ISmartAlarmAndroidSensorData,
          self).__init__(data_type=self.DATA_TYPE)
    self.sensor_id = None
    self.action = None
    self.operator = None
    self.name = None


class ISmartAlarmAndroidUserData(events.EventData):
  """iSmartAlarm on Android user event data.

  Attributes:
    id (int): user identifier.
    action (int): user action code.
  """

  DATA_TYPE = 'ismartalarm:android:userevent'

  def __init__(self):
    """Initializes event data."""
    super(ISmartAlarmAndroidUserData,
          self).__init__(data_type=self.DATA_TYPE)
    self.id = None
    self.action = None


class ISmartAlarmAndroidPlugin(interface.SQLitePlugin):
  """Parser plugin for ISmartAlarm on Android."""

  NAME = 'ismartalarm_android'
  DESCRIPTION = 'Parser for iSmartAlarm on android database'

  QUERIES = [
      (('SELECT date, action, IPUID as ipu_id, operator, profileid AS profile_id, '
        'profileName AS profile_name FROM tb_ipudairy'), 'ParseIpuDairyRow'),
      ('SELECT sensorId AS sensor_id, date, action, operator, name FROM tb_sensordairy',
       'ParseSensorDairyRow'),
      ('SELECT id, date, action FROM tb_userdairy', 'ParseUserDairyRow')
    ]

  REQUIRED_TABLES = frozenset(['TB_IPUDairy', 'TB_SensorDairy', 'TB_userDairy'])

  SCHEMAS = [{
      'TB_CameraDairy': (
          'CREATE TABLE TB_CameraDairy (cameraID varchar(20,0) , date '
          'int(8,0) default 0, userName varchar(64,0), logType int(4,0))'),
      'TB_CountryInfo': (
          'CREATE TABLE TB_CountryInfo (countryId int(4,0) PRIMARY KEY , '
          'countryName varchar(128,0), countryTelNum varchar(20,0), '
          'countryForShort varchar(128,0), isAvaiable varchar(10,0) , '
          'deviceEdition varchar(128,0) )'),
      'TB_IPUDairy': (
          'CREATE TABLE TB_IPUDairy (date int(8,0) default 0 , action '
          'varchar(10,0), IPUID varchar(20,0), logType int(4,0), sensorName '
          'varchar(64,0) , operator varchar(128,0) ,sensorType int(4,0), '
          'sensorID varchar(20,0), userID varchar(20,0) , profileid '
          'varchar(10,0) , profileName varchar(256,0) )'),
      'TB_IPUVersionInfo': (
          'CREATE TABLE TB_IPUVersionInfo (IPUVerId int(4,0) PRIMARY KEY , '
          'Ver varchar(50,0), Ip varchar(20,0), isOpened varchar(10,0))'),
      'TB_ISC3Dairy': (
          'CREATE TABLE TB_ISC3Dairy (iSC3Id varchar(20,0) , logType int(4,0) '
          ', date int(8,0) default 0, action varchar(512,0), alarmType '
          'int(4,0))'),
      'TB_ISC3VideoInfo': (
          'CREATE TABLE TB_ISC3VideoInfo(id INTEGER PRIMARY KEY AUTOINCREMENT '
          ', ISC3ID varchar(20,0) , ipuMac varchar(20,0), videoUrl '
          'varchar(512,0), picUrl varchar(512,0), isc3Timezone varchar(20,0), '
          'ipuFileGroup varchar(20,0) , isc3FileGroup varchar(20,0) , '
          'localVideoPath varchar(512,0), localPicPath varchar(512,0) , ts '
          'int(8,0) , accessTs int(8,0), readStatus varchar(20,0) )'),
      'TB_PushMessageInfo': (
          'CREATE TABLE TB_PushMessageInfo (messageID varchar(128,0) PRIMARY '
          'KEY , Content varchar(512,0), IPUID varchar(20,0), readstatus '
          'int(4,0) default 0, happenTime int(8,0) default 0, receiveTime '
          'int(8,0) default 0 , userTel varchar(20,0) ,messageName '
          'varchar(512,0) ,deviceType varchar(20,0) default 0 ,homeID '
          'varchar(128,0) )'),
      'TB_SensorDairy': (
          'CREATE TABLE TB_SensorDairy (sensorID varchar(20,0) , date '
          'int(8,0) default 0, action varchar(512,0), conectStatus int(4,0), '
          'model varchar(128,0),operator varchar(64,0),name '
          'varchar(256,0),logtype varchar(10,0))'),
      'TB_camera': (
          'CREATE TABLE TB_camera (id varchar(20,0) PRIMARY KEY , argue '
          'varchar(256,0), nickName varchar(512,0) , cameraDNS varchar(512,0) '
          ',cameraType varchar(20,0) ,cameraIP varchar(256,0), cameraPort '
          'INT(8,0) , cameraUserName varchar(512,0) ,password varchar(512,0) '
          ',ipuId varchar(20,0) )'),
      'TB_ipuInfo': (
          'CREATE TABLE TB_ipuInfo(id varchar(20,0) PRIMARY KEY , name '
          'varchar(256,0) , hardwareVersion varchar(20,0), firmwareVersion '
          'varchar(20,0), productModel varchar(20,0), ip varchar(64,0), '
          'timezone varchar(20,0) , displayName varchar(256,0) , workBegin '
          'varchar(20,0), workEnd varchar(20,0), ssid varchar(512,0), '
          'panicStatus varchar(8,0), longitude varchar(128,0) , latitude '
          'varchar(128,0) , productNum varchar(20,0), address varchar(512,0), '
          'updateStatus varchar(8,0), regional varchar(128,0), spectrum '
          'varchar(128,0) , locking varchar(8,0) , phones varchar(512,0), '
          'hasEnr int(4,0), enr varchar(20,0), isBound int(4,0), '
          'runningProfileId varchar(20,0) , displayProfileId varchar(20,0) , '
          'unReadMsgNum varchar(20,0), updateRate varchar(10,0) )'),
      'TB_isc3Info': (
          'CREATE TABLE TB_isc3Info(id varchar(20,0) PRIMARY KEY , nickName '
          'varchar(256,0) , enr varchar(20,0), uid varchar(20,0), ssid '
          'varchar(256,0), ip varchar(64,0), soundAlarm varchar(8,0) , '
          'moveAlarm varchar(8,0) , pushSwitch varchar(8,0), '
          'distinguishAbility varchar(8,0) , lightStatus varchar(8,0) , '
          'soundSensitivity varchar(8,0) , moveSensitivity varchar(8,0), '
          'ipuId varchar(20,0) , hardwareVersion varchar(32,0) , '
          'firmwareVersion varchar(32,0) , productModel varchar(32,0), '
          'productNum varchar(32,0) , tcpPort int(8,0))'),
      'TB_logoInfo': (
          'CREATE TABLE TB_logoInfo (hostKey varchar(50,0) PRIMARY KEY , '
          'remoteUrl varchar(256,0), localPath varchar(256,0), Ts int(8,0) '
          'default 0)'),
      'TB_profileIcamera': (
          'CREATE TABLE TB_profileIcamera (id INTEGER PRIMARY KEY '
          'AUTOINCREMENT , icameraId varchar(20,0), profileId varchar(20,0) , '
          'icameraType varchar(8,0) ,soundAlarm varchar(20,0) ,motionAlarm '
          'varchar(20,0), icameraNickName varchar(512,0))'),
      'TB_profileInfo': (
          'CREATE TABLE TB_profileInfo (id varchar(20,0) PRIMARY KEY , name '
          'varchar(256,0), runStatus varchar(8,0) , displayStatus '
          'varchar(8,0) ,ipuId varchar(20,0) )'),
      'TB_profileSensor': (
          'CREATE TABLE TB_profileSensor (id INTEGER PRIMARY KEY '
          'AUTOINCREMENT , sensorId varchar(20,0), profileId varchar(20,0) , '
          'sensorStatus varchar(8,0) ,sensorType int(8,0) ,sensorNickName '
          'varchar(512,0))'),
      'TB_screenshotsInfo': (
          'CREATE TABLE TB_screenshotsInfo (id INTEGER PRIMARY KEY '
          'AUTOINCREMENT , cameraMac varchar(20,0), picPath varchar(256,0), '
          'userTel varchar(64,0), ts int(8,0) default 0)'),
      'TB_sensorInfo': (
          'CREATE TABLE TB_sensorInfo(mac varchar(20,0) PRIMARY KEY , name '
          'varchar(256,0) , type int(8,0), id varchar(20,0) , status '
          'varchar(8,0) , power varchar(8,0), ts varchar(20,0), connectStatus '
          'varchar(8,0), model varchar(20,0), ledStatus varchar(8,0) , color '
          'varchar(8,0) , custom varchar(256,0), synStatus varchar(8,0) , '
          'ipuId varchar(20,0) , armType varchar(8,0) , modifyStatus '
          'varchar(8,0) )'),
      'TB_updatedevice': (
          'CREATE TABLE TB_updatedevice (id INTEGER PRIMARY KEY AUTOINCREMENT '
          ', mac varchar(20,0), firmversion varchar(20,0), updatetime '
          'varchar(20,0) , isneedupdate varchar(20,0))'),
      'TB_userDairy': (
          'CREATE TABLE TB_userDairy (id varchar(20,0) , date int(8,0) '
          'default 0, action varchar(64,0) , nickname varchar(256,0) ,ipuid '
          'varchar(20,0) )'),
      'TB_userInfo': (
          'CREATE TABLE TB_userInfo(tel varchar(20,0) , id varchar(20,0) , '
          'name varchar(256,0), pwd varchar(512,0), email varchar(512,0), '
          'language varchar(20,0), ts int(8,0) , countryCode varchar(20,0) , '
          'jurisdiction varchar(10,0), inhome varchar(10,0) , remoteControl '
          'varchar(10,0))'),
      'TB_user_icamera': (
          'CREATE TABLE TB_user_icamera (id INTEGER PRIMARY KEY AUTOINCREMENT '
          ', tel varchar(20,0) , cameraMac varchar(20,0))'),
      'TB_user_ipu': (
          'CREATE TABLE TB_user_ipu (id INTEGER PRIMARY KEY AUTOINCREMENT , '
          'tel varchar(20,0), ipuId varchar(20,0) , permission varchar(20,0))'),
      'android_metadata': (
          'CREATE TABLE android_metadata (locale TEXT)')
}]

  def ParseIpuDairyRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses an IPU row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row resulting from query.
    """
    query_hash = hash(query)

    event_data = ISmartAlarmAndroidIpuData()
    event_data.query = query
    event_data.action = self._GetRowValue(query_hash, row, 'action')
    event_data.ipu_id = self._GetRowValue(query_hash, row, 'ipu_id')
    event_data.operator = self._GetRowValue(query_hash, row, 'operator')
    event_data.profile_id = self._GetRowValue(query_hash, row, 'profile_id')
    event_data.profile_name = self._GetRowValue(query_hash, row, 'profile_name')

    timestamp = self._GetRowValue(query_hash, row, 'date')
    if timestamp:
      date_time = dfdatetime_java_time.JavaTime(timestamp=self.FixTimestamp(timestamp))
      logger.debug('IpuEvent: {0}'.format(date_time.CopyToDateTimeStringISO8601()))
      event = time_events.DateTimeValuesEvent(
          date_time, definitions.TIME_DESCRIPTION_CREATION)
      parser_mediator.ProduceEventWithEventData(event, event_data)

  def ParseSensorDairyRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses a sensor event row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row resulting from query.
    """
    query_hash = hash(query)

    event_data = ISmartAlarmAndroidSensorData()
    event_data.query = query
    event_data.sensor_id = self._GetRowValue(query_hash, row, 'sensor_id')
    event_data.action = self._GetRowValue(query_hash, row, 'action')
    event_data.operator = self._GetRowValue(query_hash, row, 'operator')
    event_data.name = self._GetRowValue(query_hash, row, 'name')

    timestamp = self._GetRowValue(query_hash, row, 'date')
    if timestamp:
      date_time = dfdatetime_java_time.JavaTime(timestamp=self.FixTimestamp(timestamp))
      logger.debug('SensorEvent: {0}'.format(date_time.CopyToDateTimeStringISO8601()))
      event = time_events.DateTimeValuesEvent(
          date_time, definitions.TIME_DESCRIPTION_CREATION)
      parser_mediator.ProduceEventWithEventData(event, event_data)

  def ParseUserDairyRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses a status row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row resulting from query.
    """
    query_hash = hash(query)

    event_data = ISmartAlarmAndroidUserData()
    event_data.query = query
    event_data.id = self._GetRowValue(query_hash, row, 'id')
    event_data.action = self._GetRowValue(query_hash, row, 'action')

    timestamp = self._GetRowValue(query_hash, row, 'date')
    if timestamp:
      date_time = dfdatetime_java_time.JavaTime(timestamp=self.FixTimestamp(timestamp))
      logger.debug('UserEvent: {0}'.format(date_time.CopyToDateTimeStringISO8601()))
      event = time_events.DateTimeValuesEvent(
          date_time, definitions.TIME_DESCRIPTION_CREATION)
      parser_mediator.ProduceEventWithEventData(event, event_data)

  def FixTimestamp(self, timestamp):
    """Adjusts for second-resolution timestamps

    iSmartAlarm is inconsistent in how it stores timestamps, even within a single table.
    Args:
      timestamp (int): a unix epoch timestamp in seconds or milliseconds
    Returns:
       (int): a unix expoch timestamp in milliseconds
    """
    if timestamp < 9999999999 and timestamp != 0:
      timestamp = timestamp * 1000
    return timestamp


sqlite.SQLiteParser.RegisterPlugin(ISmartAlarmAndroidPlugin)

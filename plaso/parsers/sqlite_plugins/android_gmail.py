# -*- coding: utf-8 -*-
"""This file contains a parser for the Google Hangouts Active Conversations DB.
/userdata/data/com.google.android.gm/databases/mailstore.username@gmail.com
This SQLite database is the e-mail database for gmail
"""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface
import zlib

class GmailMessagesData(events.EventData):
  """GMail Mail event data.

  Attributes:
    fromAddress (str): Name with the sender.
    to (str): Name with the reciver.
    cc (str): Name with the cc.
    bcc (str): Name with the bcc.
    replyToAddresses (str): name with the reply to ccAddresses
    subject (str): subject of the e-mail
    snippet (str): snippet of the e-mail
    body (str): content of the SMS text message.
  """

  DATA_TYPE = 'android:messaging:gmail'

  def __init__(self):
    """Initializes event data."""
    super(GmailMessagesData, self).__init__(data_type=self.DATA_TYPE)
    self.fromAddress = None
    self.to = None
    self.cc = None
    self.bcc = None
    self.replyToAddresses = None
    self.subject = None
    self.snippet = None
    self.body = None


class GmailMessagePlugin(interface.SQLitePlugin):
  """Parser for Gmail database."""

  NAME = 'gmail_messages'
  DESCRIPTION = 'Parser for Android Gmail Messages SQLite database files.'

  # Define the needed queries.
  QUERIES = [
      ('SELECT fromAddress,toAddresses,ccAddresses,bccAddresses,'
      'replyToAddresses,dateSentMs,dateReceivedMs,subject,snippet,'
      'bodyCompressed from messages;', 'ParseMessagesRow')]

  # The required tables.
  REQUIRED_TABLES = frozenset(['messages'])

  SCHEMAS = [{
        'ads': (
          'CREATE TABLE ads (_id INTEGER PRIMARY KEY, event_id TEXT, '
          'advertiser_name TEXT, title TEXT, line1 TEXT, visible_url TEXT, '
          'advertiser_image_data BLOB, body TEXT, expiration INTEGER, reason '
          'INTEGER, apm_extra_targeting_data TEXT, starred INTEGER, '
          'view_status INTEGER, view TEXT, slot TEXT, apm_xsrf_token TEXT, '
          'delete_status INTEGER DEFAULT 0, redirect_url TEXT, wta_data TEXT, '
          'view_url TEXT, click_url TEXT, interaction_url TEXT, '
          'body_view_urls TEXT, obfuscated_data TEXT, report_ad_server '
          'INTEGER, report_bow INTEGER, send_body INTEGER, '
          'show_body_feedback_survey INTEGER, '
          'report_duration_since_last_action INTEGER DEFAULT 0, click_id '
          'TEXT, aia_star_rating TEXT, aia_ratings_count INTEGER, '
          'aia_package_name TEXT, aia_inline_install_enabled INTEGER, '
          'aia_teaser_experiment INTEGER, aia_body_experiment INTEGER, '
          'dismiss_survey_data TEXT, aia_referrer TEXT, aia_install_url TEXT, '
          'aia_install_button_url TEXT, last_shown_timestamp INTEGER DEFAULT '
          '0, last_clicked_timestamp INTEGER DEFAULT 0, '
          'last_starred_timestamp INTEGER DEFAULT 0, wta_get_url TEXT, '
          'wta_tooltip_type INTEGER DEFAULT 0, tab INTEGER DEFAULT 0, '
          'ad_client_dedup_id_data TEXT, '
          'report_duration_since_last_action_to_bow INTEGER DEFAULT 0, '
          'report_click_id_for_click_event INTEGER DEFAULT 0, '
          'aia_enable_soy_generated_body_format INTEGER DEFAULT 0, '
          'duffy_options TEXT, duffy_config TEXT, duffy_submitted INTEGER '
          'DEFAULT 0, stylesheet TEXT, stylesheet_restrictor TEXT, ad_options '
          'TEXT, duffy_teaser_config TEXT, duffy_teaser_submitted INTEGER '
          'DEFAULT 0, duffy_teaser_options TEXT, ad_body_cml_data BLOB, '
          'duffy_body_second_step_options TEXT, '
          'duffy_body_second_step_submitted INTEGER DEFAULT 0, '
          'UNIQUE(event_id))'),
      'android_metadata': (
          'CREATE TABLE android_metadata (locale TEXT)'),
      'attachments': (
          'CREATE TABLE attachments ( _id INTEGER PRIMARY KEY, '
          'messages_conversation INTEGER, messages_messageId INTEGER, '
          'messages_partId TEXT, originExtras TEXT, desiredRendition TEXT, '
          'automatic INTEGER, downloadedRendition TEXT, downloadId INTEGER, '
          'status TEXT, saveToSd INTEGER, filename TEXT, priority INTEGER '
          'DEFAULT 0, mimeType TEXT DEFAULT NULL, size INTEGER DEFAULT 0, '
          'UNIQUE( messages_conversation, messages_messageId, '
          'messages_partId, desiredRendition, saveToSd), '
          'UNIQUE(messages_messageId, messages_partId, desiredRendition, '
          'saveToSd))'),
      'blocked_senders': (
          'CREATE TABLE blocked_senders(creationTimeMs INTEGER NOT NULL '
          'DEFAULT 0, senderIdentifier TEXT, displayName TEXT, '
          'UNIQUE(senderIdentifier))'),
      'conversation_labels': (
          'CREATE TABLE conversation_labels ( labels_id TEXT, queryId '
          'INTEGER, isZombie INTEGER, sortMessageId INTEGER, date INTEGER, '
          'conversation_id INTEGER, UNIQUE(labels_id, queryId, '
          'conversation_id))'),
      'conversations': (
          'CREATE TABLE conversations (_id INTEGER, queryId INTEGER, subject '
          'TEXT, snippet TEXT, fromAddress TEXT, fromProtoBuf '
          'BLOB,fromCompact BLOB,personalLevel INTEGER, labelIds TEXT, '
          'numMessages INTEGER, maxMessageId INTEGER, hasAttachments INTEGER, '
          'hasMessagesWithErrors INTEGER, syncRationale TEXT, '
          'syncRationaleMessageId INTEGER, forceAllUnread INTEGER, dirty '
          'INTEGER DEFAULT 0, unreadMessageId INTEGER DEFAULT 0, '
          'unreadMessageLocalId INTEGER DEFAULT 0, attachmentPreviews TEXT '
          'DEFAULT NULL, attachmentPreviewStates INTEGER DEFAULT 0, '
          'attachmentPreviewsCount INTEGER DEFAULT 0, permalink TEXT DEFAULT '
          'NULL, unsubscribeSenderName TEXT DEFAULT NULL, promoteCalendar '
          'INTEGER DEFAULT 0, unsubscribeSenderIdentifier TEXT DEFAULT NULL, '
          'fromCompactV2 BLOB, hasCalendarInvite INTEGER DEFAULT 0, '
          'hasWalletAttachment INTEGER DEFAULT 0, serverPermId TEXT DEFAULT '
          'NULL, fromCompactV3 BLOB, UNIQUE(_id, queryId))'),
      'conversations_to_fetch': (
          'CREATE TABLE conversations_to_fetch (_id INTEGER PRIMARY KEY, '
          'nextAttemptDateMs INTEGER DEFAULT 0, numAttempts INTEGER DEFAULT '
          '0)'),
      'custom_from_prefs': (
          'CREATE TABLE custom_from_prefs ( _id TEXT PRIMARY KEY, name TEXT, '
          'address TEXT, is_default TEXT, reply_to TEXT)'),
      'custom_label_color_prefs': (
          'CREATE TABLE custom_label_color_prefs ( _id INTEGER PRIMARY KEY, '
          'color_index TEXT, text_color TEXT, background_color TEXT)'),
      'dasher_info': (
          'CREATE TABLE dasher_info ( _id INTEGER PRIMARY KEY, domainTitle '
          'TEXT)'),
      'drive_operations': (
          'CREATE TABLE drive_operations (_id INTEGER PRIMARY KEY '
          'AUTOINCREMENT,save INTEGER,message TEXT,attachment TEXT,retries '
          'INTEGER, conversation INTEGER, blocking INTEGER)'),
      'engine_settings': (
          'CREATE TABLE engine_settings (_id INTEGER PRIMARY KEY,name '
          'TEXT,value TEXT,UNIQUE (name))'),
      'labels': (
          'CREATE TABLE labels ( _id INTEGER PRIMARY KEY, canonicalName TEXT, '
          'name TEXT, numConversations TEXT, numUnreadConversations TEXT, '
          'color INTEGER DEFAULT 2147483647, systemLabel INTEGER DEFAULT 0, '
          'systemLabelOrder INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0, '
          'labelCountDisplayBehavior INTEGER DEFAULT 0, labelSyncPolicy '
          'INTEGER DEFAULT 0, visibility TEXT, lastTouched INTEGER DEFAULT 0, '
          'numUnseenConversations INTEGER DEFAULT 0, lastMessageTimestamp '
          'INTEGER NOT NULL DEFAULT 0)'),
      'message_labels': (
          'CREATE TABLE message_labels (_id INTEGER PRIMARY KEY,labels_id '
          'INTEGER not null,message_messageId INTEGER not '
          'null,message_conversation INTEGER,UNIQUE (labels_id, '
          'message_messageId))'),
      'messages': (
          'CREATE TABLE messages (_id INTEGER PRIMARY KEY,messageId '
          'INTEGER,conversation INTEGER,fromAddress TEXT,toAddresses '
          'TEXT,ccAddresses TEXT,bccAddresses TEXT,replyToAddresses '
          'TEXT,dateSentMs INTEGER,dateReceivedMs INTEGER,subject '
          'TEXT,snippet TEXT,listInfo TEXT,personalLevel INTEGER,body '
          'TEXT,bodyEmbedsExternalResources INTEGER,joinedAttachmentInfos '
          'TEXT,synced INTEGER,error TEXT, clientCreated INTEGER, '
          'refMessageId INTEGER DEFAULT 0, forward INTEGER DEFAULT 0, '
          'includeQuotedText INTEGER DEFAULT 0, quoteStartPos INTEGER DEFAULT '
          '0, bodyCompressed BLOB DEFAULT NULL, customFromAddress TEXT '
          'DEFAULT NULL, queryId INTEGER DEFAULT 1, spamDisplayedReasonType '
          'INTEGER DEFAULT -1,deliveryChannel '
          'INTEGER,referencesRfc822MessageIds '
          'TEXT,showSendersFullEmailAddress INTEGER,viaDomain '
          'TEXT,showForgedFromMeWarning INTEGER,refAdEventId TEXT,permalink '
          'TEXT,clipped INTEGER DEFAULT 0,encrypted INTEGER NOT NULL DEFAULT '
          '0,signed INTEGER NOT NULL DEFAULT 0,receivedWithTls INTEGER NOT '
          'NULL DEFAULT 0,clientDomain TEXT DEFAULT '
          'NULL,unsubscribeSenderName TEXT DEFAULT '
          'NULL,unsubscribeSenderIdentifier TEXT DEFAULT NULL,syncBlocked '
          'INTEGER NOT NULL DEFAULT 0,hasEvent INTEGER DEFAULT 0,stylesheet '
          'TEXT,stylesheetRestrictor TEXT,eventTitle TEXT DEFAULT '
          'NULL,startTime INTEGER,endTime INTEGER,allDay INTEGER DEFAULT '
          '0,location TEXT DEFAULT NULL,organizer TEXT DEFAULT NULL,attendees '
          'TEXT DEFAULT NULL,icalMethod INTEGER DEFAULT 8,eventId TEXT '
          'DEFAULT NULL,calendarId TEXT DEFAULT NULL,responder TEXT DEFAULT '
          'NULL,responseStatus INTEGER DEFAULT 0,spf TEXT DEFAULT NULL,dkim '
          'TEXT DEFAULT NULL, certificateSubject TEXT DEFAULT NULL, '
          'certificateIssuer TEXT DEFAULT NULL, certificateValidSinceSec '
          'INTEGER DEFAULT 0, certificateValidUntilSec INTEGER DEFAULT 0, '
          'mailJsBody TEXT, enhancedRecipients TEXT DEFAULT NULL, '
          'walletAttachmentId INTEGER DEFAULT 0, hasSRSIntent INTEGER DEFAULT '
          '0, srsTimeCoords TEXT, untrustedAddresses TEXT, hasMJWs INTEGER '
          'DEFAULT 0, outboundEncryptionSupport INTEGER NOT NULL DEFAULT 0, '
          'rfcId TEXT DEFAULT NULL, messageServerPermId TEXT, '
          'threadServerPermId TEXT, displayNameIfSuspicious TEXT DEFAULT '
          'NULL,UNIQUE(messageId))'),
      'messages_to_fetch': (
          'CREATE TABLE messages_to_fetch (_id INTEGER PRIMARY KEY)'),
      'operations': (
          'CREATE TABLE operations (_id INTEGER PRIMARY KEY '
          'AUTOINCREMENT,action TEXT,message_messageId INTEGER,value1 '
          'INTEGER,value2 INTEGER, numAttempts INTEGER DEFAULT 0, '
          'nextTimeToAttempt INTEGER DEFAULT 0, delay INTEGER DEFAULT 0, '
          'value3 TEXT, value4 TEXT, value5 TEXT, value6 TEXT, value7 TEXT, '
          'value8 TEXT, value9 TEXT, value10 TEXT, value11 TEXT, value12 TEXT '
          ', value13 TEXT, value14 TEXT, value15 TEXT, value16 TEXT, value17 '
          'TEXT, value18 TEXT, value19 TEXT, value20 TEXT)'),
      'promo_offers': (
          'CREATE TABLE promo_offers (conversation_id INTEGER PRIMARY KEY, '
          'expiration_time_millis INTEGER, coupon_code TEXT, discount_percent '
          'INTEGER, score INTEGER, earliest_trigger_time_millis INTEGER, '
          'merchant_name TEXT, unseen INTEGER, pending_delete INTEGER, '
          'show_expiration_time INTEGER, obfuscated_data TEXT, '
          'merchant_logo_url TEXT, show_merchant_logo_on_email_teaser '
          'INTEGER, discount_description TEXT, image_url TEXT, '
          'UNIQUE(conversation_id))'),
      'promotions': (
          'CREATE TABLE promotions (_id INTEGER PRIMARY KEY, priority '
          'INTEGER, startTime INTEGER, expirationTime INTEGER, titleText '
          'TEXT, bodyText TEXT, bodyHtml TEXT, positiveButtonText TEXT, '
          'negativeButtonText TEXT, buttonUrl TEXT, rawImageData BLOB, '
          'minBuildSdk INTEGER)'),
      's10s': (
          'CREATE TABLE s10s (message_id INTEGER PRIMARY KEY,r1 TEXT DEFAULT '
          'NULL,r2 TEXT DEFAULT NULL,r3 TEXT DEFAULT NULL, drop_index INTEGER '
          'DEFAULT -1, tags1 TEXT DEFAULT NULL, tags2 TEXT DEFAULT NULL, '
          'tags3 TEXT DEFAULT NULL)'),
      'save_to_drive': (
          'CREATE TABLE save_to_drive (_id INTEGER PRIMARY KEY '
          'AUTOINCREMENT,driveAccount TEXT,messageKey INTEGER,resourceId '
          'TEXT,uploaded INTEGER,placeholder INTEGER,blocking '
          'INTEGER,oldAccount TEXT,oldSaveId INTEGER DEFAULT -1)'),
      'search_sequence': (
          'CREATE TABLE search_sequence ( _id INTEGER PRIMARY KEY '
          'AUTOINCREMENT, type INTEGER NOT NULL DEFAULT 0, action INTEGER NOT '
          'NULL DEFAULT 0, messageId INTEGER NOT NULL DEFAULT 0, '
          'conversationId INTEGER NOT NULL DEFAULT 0, labelId INTEGER NOT '
          'NULL DEFAULT 0)'),
      'search_status': (
          'CREATE TABLE search_status (_id INTEGER PRIMARY KEY, '
          'app_data_search_enabled INTEGER, incarnation TEXT, seqnos_trimmed '
          'INTEGER)'),
      'send_without_sync_conversations_to_fetch': (
          'CREATE TABLE send_without_sync_conversations_to_fetch (_id INTEGER '
          'PRIMARY KEY)'),
      'server_preferences': (
          'CREATE TABLE server_preferences ( _id TEXT PRIMARY KEY, name TEXT, '
          'value TEXT, blobValue BLOB DEFAULT NULL)'),
      'sync_settings': (
          'CREATE TABLE sync_settings (_id INTEGER PRIMARY KEY,name '
          'TEXT,value TEXT,UNIQUE (name))'),
      'unsubscribed_senders': (
          'CREATE TABLE unsubscribed_senders (creationTimeMs INTEGER NOT NULL '
          'DEFAULT 0, senderIdentifier TEXT, UNIQUE(senderIdentifier))'),
      'wallet_attachments': (
          'CREATE TABLE wallet_attachments (_id INTEGER PRIMARY KEY '
          'AUTOINCREMENT,draftToken TEXT,transactionId TEXT,amount '
          'INTEGER,currencyCode TEXT,transferType INTEGER,htmlSnippet '
          'TEXT,htmlSignature TEXT)')}]


  def ParseMessagesRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses an Messages row.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row.
    """
    query_hash = hash(query)

    event_data = GmailMessagesData()

    event_data.fromAddress = self._GetRowValue(query_hash, row, 'fromAddress')
    event_data.to = self._GetRowValue(query_hash, row, 'toAddresses')
    event_data.cc = self._GetRowValue(query_hash, row, 'ccAddresses')
    event_data.bcc = self._GetRowValue(query_hash, row, 'bccAddresses')
    event_data.replyToAddresses = self._GetRowValue(query_hash, row, 'replyToAddresses')
    event_data.subject = self._GetRowValue(query_hash, row, 'subject')
    event_data.query = query

    timestamp = self._GetRowValue(query_hash, row, 'dateSentMs')
    date_time = dfdatetime_posix_time.PosixTimeInMicroseconds(
        timestamp=timestamp)

    event = time_events.DateTimeValuesEvent(
        date_time, definitions.TIME_DESCRIPTION_CREATION)
    parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(GmailMessagePlugin)

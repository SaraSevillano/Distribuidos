 #!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
'''
Managing topic implementacion
'''
import IceStorm

class ManageTopics:

    def __init__(self, broker, topic_room_manager=None):
        self.broker = broker
        self.topic_mgr = self.create_topic_manager()
        self.topic_room_manager = self.create_topic_event(self.topic_mgr, topic_room_manager)
    def create_topic_manager(self):
        ''' Create topic manager '''
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.broker.propertyToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

    def create_topic_event(self, topic_mgr, topic_name):
        ''' Create topic event '''
        try:
            return topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            return topic_mgr.create(topic_name)
    
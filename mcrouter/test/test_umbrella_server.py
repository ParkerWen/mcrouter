# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from mcrouter.test.MCProcess import MockMemcached
from mcrouter.test.McrouterTestCase import McrouterTestCase


class TestUmbrellaServer(McrouterTestCase):
    config_mc = './mcrouter/test/test_umbrella_server_mc.json'
    config = './mcrouter/test/test_umbrella_server.json'
    extra_args = []

    def setUp(self):
        self.mc = self.add_server(MockMemcached())
        self.mcrouter_mc = self.add_mcrouter(
            self.config_mc,
            extra_args=self.extra_args,
            bg_mcrouter=True)
        self.mcrouter = self.add_mcrouter(
            self.config,
            extra_args=self.extra_args)

    def test_umbrella_server(self):
        key = 'foo'
        value = 'value'
        self.mcrouter.set(key, value)
        self.assertEqual(self.mcrouter.get(key), value)
        self.assertEqual(self.mc.get(key), value)

    def test_umbrella_server_touch(self):
        key = 'foo'
        value = 'value'
        self.assertIsNone(self.mcrouter.get(key))
        self.assertEqual(self.mcrouter.touch(key, 100), "NOT_FOUND")
        self.mcrouter.set(key, value)
        self.assertEqual(self.mcrouter.get(key), value)
        self.assertEqual(self.mcrouter.touch(key, 100), "TOUCHED")

    def test_umbrella_server_append_prepend(self):
        key = 'foo'
        value = 'value'
        suffix = 'abc123'
        prefix = 'xyz456'
        self.mcrouter.set(key, value)
        self.assertEqual(self.mcrouter.get(key), value)
        self.assertEqual(self.mc.get(key), value)
        self.assertEqual(self.mcrouter.append(key, suffix), "STORED")
        self.assertEqual(self.mcrouter.get(key), value + suffix)
        self.assertEqual(self.mcrouter.prepend(key, prefix), "STORED")
        self.assertEqual(self.mcrouter.get(key), prefix + value + suffix)

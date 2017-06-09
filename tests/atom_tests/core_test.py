#!/usr/bin/env python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# This module is used for version 2 of the Google Data APIs.


# __author__ = 'j.s@google.com (Jeff Scudder)'

import unittest

import lxml.etree as ElementTree
import atom.core
import gdata.test_config as conf

SAMPLE_XML = ('<outer xmlns="http://example.com/xml/1" '
              'xmlns:two="http://example.com/xml/2">'
              '<inner x="123"/>'
              '<inner x="234" y="abc"/>'
              '<inner>'
              '<two:nested>Some Test</two:nested>'
              '<nested>Different Namespace</nested>'
              '</inner>'
              '<other two:z="true"></other>'
              '</outer>')

NO_NAMESPACE_XML = ('<foo bar="123"><baz>Baz Text!</baz></foo>')

V1_XML = ('<able xmlns="http://example.com/1" '
          'xmlns:ex="http://example.com/ex/1">'
          '<baker foo="42"/>'
          '<ex:charlie>Greetings!</ex:charlie>'
          '<same xmlns="http://example.com/s" x="true">'
          '</able>')

V2_XML = ('<alpha xmlns="http://example.com/2" '
          'xmlns:ex="http://example.com/ex/2">'
          '<bravo bar="42"/>'
          '<ex:charlie>Greetings!</ex:charlie>'
          '<same xmlns="http://example.com/s" x="true">'
          '</alpha>')


class Child(atom.core.XmlElement):
    _qname = ('{http://example.com/1}child', '{http://example.com/2}child')


class Foo(atom.core.XmlElement):
    _qname = 'foo'


class Example(atom.core.XmlElement):
    _qname = '{http://example.com}foo'
    child = Child
    foos = [Foo]
    tag = 'tag'
    versioned_attr = ('attr', '{http://new_ns}attr')


# Example XmlElement subclass declarations.
class Inner(atom.core.XmlElement):
    _qname = '{http://example.com/xml/1}inner'
    my_x = 'x'


class Outer(atom.core.XmlElement):
    _qname = '{http://example.com/xml/1}outer'
    innards = [Inner]


class XmlElementTest(unittest.TestCase):
    def testGetQName(self):
        class Unversioned(atom.core.XmlElement):
            _qname = '{http://example.com}foo'

        class Versioned(atom.core.XmlElement):
            _qname = ('{http://example.com/1}foo', '{http://example.com/2}foo')

        self.assertTrue(
            atom.core._get_qname(Unversioned, 1) == '{http://example.com}foo')
        self.assertTrue(
            atom.core._get_qname(Unversioned, 2) == '{http://example.com}foo')
        self.assertTrue(
            atom.core._get_qname(Versioned, 1) == '{http://example.com/1}foo')
        self.assertTrue(
            atom.core._get_qname(Versioned, 2) == '{http://example.com/2}foo')

    def testConstructor(self):
        e = Example()
        self.assertTrue(e.child is None)
        self.assertTrue(e.tag is None)
        self.assertTrue(e.versioned_attr is None)
        self.assertTrue(e.foos == [])
        self.assertTrue(e.text is None)

    def testGetRules(self):
        rules1 = Example._get_rules(1)
        self.assertTrue(rules1[0] == '{http://example.com}foo')
        self.assertTrue(rules1[1]['{http://example.com/1}child'] == ('child', Child,
                                                                     False))
        self.assertTrue(rules1[1]['foo'] == ('foos', Foo, True))
        self.assertTrue(rules1[2]['tag'] == 'tag')
        self.assertTrue(rules1[2]['attr'] == 'versioned_attr')
        # Check to make sure we don't recalculate the rules.
        self.assertTrue(rules1 == Example._get_rules(1))
        rules2 = Example._get_rules(2)
        self.assertTrue(rules2[0] == '{http://example.com}foo')
        self.assertTrue(rules2[1]['{http://example.com/2}child'] == ('child', Child,
                                                                     False))
        self.assertTrue(rules2[1]['foo'] == ('foos', Foo, True))
        self.assertTrue(rules2[2]['tag'] == 'tag')
        self.assertTrue(rules2[2]['{http://new_ns}attr'] == 'versioned_attr')

    def testGetElements(self):
        e = Example()
        e.child = Child()
        e.child.text = 'child text'
        e.foos.append(Foo())
        e.foos[0].text = 'foo1'
        e.foos.append(Foo())
        e.foos[1].text = 'foo2'
        e._other_elements.append(atom.core.XmlElement())
        e._other_elements[0]._qname = 'bar'
        e._other_elements[0].text = 'other1'
        e._other_elements.append(atom.core.XmlElement())
        e._other_elements[1]._qname = 'child'
        e._other_elements[1].text = 'other2'

        self.contains_expected_elements(e.get_elements(),
                                        ['foo1', 'foo2', 'child text', 'other1', 'other2'])
        self.contains_expected_elements(e.get_elements('child'),
                                        ['child text', 'other2'])
        self.contains_expected_elements(
            e.get_elements('child', 'http://example.com/1'), ['child text'])
        self.contains_expected_elements(
            e.get_elements('child', 'http://example.com/2'), [])
        self.contains_expected_elements(
            e.get_elements('child', 'http://example.com/2', 2), ['child text'])
        self.contains_expected_elements(
            e.get_elements('child', 'http://example.com/1', 2), [])
        self.contains_expected_elements(
            e.get_elements('child', 'http://example.com/2', 3), ['child text'])
        self.contains_expected_elements(e.get_elements('bar'), ['other1'])
        self.contains_expected_elements(e.get_elements('bar', version=2),
                                        ['other1'])
        self.contains_expected_elements(e.get_elements('bar', version=3),
                                        ['other1'])

    def contains_expected_elements(self, elements, expected_texts):
        self.assertTrue(len(elements) == len(expected_texts))
        for element in elements:
            self.assertTrue(element.text in expected_texts)

    def testConstructorKwargs(self):
        e = Example('hello', child=Child('world'), versioned_attr='1')
        self.assertTrue(e.text == 'hello')
        self.assertTrue(e.child.text == 'world')
        self.assertTrue(e.versioned_attr == '1')
        self.assertTrue(e.foos == [])
        self.assertTrue(e.tag is None)

        e = Example(foos=[Foo('1', ignored=1), Foo(text='2')], tag='ok')
        self.assertTrue(e.text is None)
        self.assertTrue(e.child is None)
        self.assertTrue(e.versioned_attr is None)
        self.assertTrue(len(e.foos) == 2)
        self.assertTrue(e.foos[0].text == '1')
        self.assertTrue(e.foos[1].text == '2')
        self.assertTrue('ignored' not in e.foos[0].__dict__)
        self.assertTrue(e.tag == 'ok')

    def testParseBasicXmlElement(self):
        element = atom.core.xml_element_from_string(SAMPLE_XML,
                                                    atom.core.XmlElement)
        inners = element.get_elements('inner')
        self.assertTrue(len(inners) == 3)
        self.assertTrue(inners[0].get_attributes('x')[0].value == '123')
        self.assertTrue(inners[0].get_attributes('y') == [])
        self.assertTrue(inners[1].get_attributes('x')[0].value == '234')
        self.assertTrue(inners[1].get_attributes('y')[0].value == 'abc')
        self.assertTrue(inners[2].get_attributes('x') == [])
        inners = element.get_elements('inner', 'http://example.com/xml/1')
        self.assertTrue(len(inners) == 3)
        inners = element.get_elements(None, 'http://example.com/xml/1')
        self.assertTrue(len(inners) == 4)
        inners = element.get_elements()
        self.assertTrue(len(inners) == 4)
        inners = element.get_elements('other')
        self.assertTrue(len(inners) == 1)
        self.assertTrue(inners[0].get_attributes(
            'z', 'http://example.com/xml/2')[0].value == 'true')
        inners = element.get_elements('missing')
        self.assertTrue(len(inners) == 0)

    def testBasicXmlElementPreservesMarkup(self):
        element = atom.core.xml_element_from_string(SAMPLE_XML,
                                                    atom.core.XmlElement)
        tree1 = ElementTree.fromstring(SAMPLE_XML)
        tree2 = ElementTree.fromstring(element.to_string())
        self.assert_trees_similar(tree1, tree2)

    def testSchemaParse(self):
        outer = atom.core.xml_element_from_string(SAMPLE_XML, Outer)
        self.assertTrue(isinstance(outer.innards, list))
        self.assertTrue(len(outer.innards) == 3)
        self.assertTrue(outer.innards[0].my_x == '123')

    def testSchemaParsePreservesMarkup(self):
        outer = atom.core.xml_element_from_string(SAMPLE_XML, Outer)
        tree1 = ElementTree.fromstring(SAMPLE_XML)
        tree2 = ElementTree.fromstring(outer.to_string())
        self.assert_trees_similar(tree1, tree2)
        found_x_and_y = False
        found_x_123 = False
        child = tree1.find('{http://example.com/xml/1}inner')
        matching_children = tree2.findall(child.tag)
        for match in matching_children:
            if 'y' in match.attrib and match.attrib['y'] == 'abc':
                if match.attrib['x'] == '234':
                    found_x_and_y = True
                self.assertTrue(match.attrib['x'] == '234')
            if 'x' in match.attrib and match.attrib['x'] == '123':
                self.assertTrue('y' not in match.attrib)
                found_x_123 = True
        self.assertTrue(found_x_and_y)
        self.assertTrue(found_x_123)

    def testGenericTagAndNamespace(self):
        element = atom.core.XmlElement(text='content')
        # Try setting tag then namespace.
        element.tag = 'foo'
        self.assertTrue(element._qname == 'foo')
        element.namespace = 'http://example.com/ns'
        self.assertTrue(element._qname == '{http://example.com/ns}foo')

        element = atom.core.XmlElement()
        # Try setting namespace then tag.
        element.namespace = 'http://example.com/ns'
        self.assertTrue(element._qname == '{http://example.com/ns}')
        element.tag = 'foo'
        self.assertTrue(element._qname == '{http://example.com/ns}foo')

    def assert_trees_similar(self, a, b):
        """Compares two XML trees for approximate matching."""
        for child in a:
            self.assertTrue(len(a.findall(child.tag)) == len(b.findall(child.tag)))
        for child in b:
            self.assertTrue(len(a.findall(child.tag)) == len(b.findall(child.tag)))
        self.assertTrue(len(a) == len(b))
        self.assertTrue(a.text == b.text)
        self.assertTrue(a.attrib == b.attrib)


class UtilityFunctionTest(unittest.TestCase):
    def testMatchQnames(self):
        self.assertTrue(atom.core._qname_matches(
            'foo', 'http://example.com', '{http://example.com}foo'))
        self.assertTrue(atom.core._qname_matches(
            None, None, '{http://example.com}foo'))
        self.assertTrue(atom.core._qname_matches(
            None, None, 'foo'))
        self.assertTrue(atom.core._qname_matches(
            None, None, None))
        self.assertTrue(atom.core._qname_matches(
            None, None, '{http://example.com}'))
        self.assertTrue(atom.core._qname_matches(
            'foo', None, '{http://example.com}foo'))
        self.assertTrue(atom.core._qname_matches(
            None, 'http://example.com', '{http://example.com}foo'))
        self.assertTrue(atom.core._qname_matches(
            None, '', 'foo'))
        self.assertTrue(atom.core._qname_matches(
            'foo', '', 'foo'))
        self.assertTrue(atom.core._qname_matches(
            'foo', '', 'foo'))
        self.assertTrue(atom.core._qname_matches(
            'foo', 'http://google.com', '{http://example.com}foo') == False)
        self.assertTrue(atom.core._qname_matches(
            'foo', 'http://example.com', '{http://example.com}bar') == False)
        self.assertTrue(atom.core._qname_matches(
            'foo', 'http://example.com', '{http://google.com}foo') == False)
        self.assertTrue(atom.core._qname_matches(
            'bar', 'http://example.com', '{http://google.com}foo') == False)
        self.assertTrue(atom.core._qname_matches(
            'foo', None, '{http://example.com}bar') == False)
        self.assertTrue(atom.core._qname_matches(
            None, 'http://google.com', '{http://example.com}foo') == False)
        self.assertTrue(atom.core._qname_matches(
            None, '', '{http://example.com}foo') == False)
        self.assertTrue(atom.core._qname_matches(
            'foo', '', 'bar') == False)


class Chars(atom.core.XmlElement):
    _qname = '{http://example.com/}chars'
    y = 'y'
    alpha = 'a'


class Strs(atom.core.XmlElement):
    _qname = '{http://example.com/}strs'
    chars = [Chars]
    delta = 'd'


def parse(string):
    return atom.core.xml_element_from_string(string, atom.core.XmlElement)


def create(tag, string):
    element = atom.core.XmlElement(text=string)
    element._qname = tag
    return element


class CharacterEncodingTest(unittest.TestCase):
    def testUnicodeInputString(self):
        # Test parsing the inner text.
        self.assertEqual(parse('<x>&#948;</x>').text, '\u03b4')
        self.assertEqual(parse('<x>\u03b4</x>').text, '\u03b4')

        # Test output valid XML.
        self.assertEqual(parse('<x>&#948;</x>').to_string(), '<x>&#948;</x>')
        self.assertEqual(parse('<x>\u03b4</x>').to_string(), '<x>&#948;</x>')

        # Test setting the inner text and output valid XML.
        e = create('x', '\u03b4')
        self.assertEqual(e.to_string(), '<x>&#948;</x>')
        self.assertEqual(e.text, '\u03b4')
        self.assertTrue(isinstance(e.text, str))
        self.assertEqual(create('x', '\xce\xb4'.decode('utf-8')).to_string(),
                         '<x>&#948;</x>')

    def testUnicodeTagsAndAttributes(self):
        # Begin with test to show underlying ElementTree behavior.
        t = ElementTree.fromstring('<del\u03b4ta>test</del\u03b4ta>'.encode('utf-8'))
        self.assertEqual(t.tag, 'del\u03b4ta')
        self.assertEqual(parse('<\u03b4elta>test</\u03b4elta>')._qname,
                         '\u03b4elta')
        # Test unicode attribute names and values.
        t = ElementTree.fromstring('<x \u03b4a="\u03b4b" />'.encode('utf-8'))
        self.assertEqual(t.attrib, {'\u03b4a': '\u03b4b'})
        self.assertEqual(parse('<x \u03b4a="\u03b4b" />').get_attributes(
            '\u03b4a')[0].value, '\u03b4b')
        x = create('x', None)
        x._other_attributes['a'] = '\u03b4elta'
        self.assertTrue(x.to_string().startswith('<x a="&#948;elta"'))

    def testUtf8InputString(self):
        # Test parsing inner text.
        self.assertEqual(parse('<x>&#948;</x>').text, '\u03b4')
        self.assertEqual(parse('<x>\u03b4</x>'.encode('utf-8')).text, '\u03b4')
        self.assertEqual(parse('<x>\xce\xb4</x>').text, '\u03b4')

        # Test output valid XML.
        self.assertEqual(parse('<x>&#948;</x>').to_string(), '<x>&#948;</x>')
        self.assertEqual(parse('<x>\u03b4</x>'.encode('utf-8')).to_string(),
                         '<x>&#948;</x>')
        self.assertEqual(parse('<x>\xce\xb4</x>').to_string(), '<x>&#948;</x>')

        # Test setting the inner text and output valid XML.
        e = create('x', '\xce\xb4')
        self.assertEqual(e.to_string(), '<x>&#948;</x>')
        # Don't change the encoding until the we convert to an XML string.
        self.assertEqual(e.text, '\xce\xb4')
        self.assertTrue(isinstance(e.text, str))
        self.assertTrue(isinstance(e.to_string(), str))
        self.assertEqual(create('x', '\u03b4'.encode('utf-8')).to_string(),
                         '<x>&#948;</x>')
        # Test attributes and values with UTF-8 inputs.
        self.assertEqual(parse('<x \xce\xb4a="\xce\xb4b" />').get_attributes(
            '\u03b4a')[0].value, '\u03b4b')

    def testUtf8TagsAndAttributes(self):
        self.assertEqual(
            parse('<\u03b4elta>test</\u03b4elta>'.encode('utf-8'))._qname,
            '\u03b4elta')
        self.assertEqual(parse('<\xce\xb4elta>test</\xce\xb4elta>')._qname,
                         '\u03b4elta')
        # Test an element with UTF-8 in the attribute value.
        x = create('x', None)
        x._other_attributes['a'] = '\xce\xb4'
        self.assertTrue(x.to_string(encoding='UTF-8').startswith('<x a="&#948;"'))
        self.assertTrue(x.to_string().startswith('<x a="&#948;"'))

    def testOtherEncodingOnInputString(self):
        BIG_ENDIAN = 0
        LITTLE_ENDIAN = 1
        # Test parsing inner text.
        self.assertEqual(parse('<x>\u03b4</x>'.encode('utf-16')).text, '\u03b4')

        # Test output valid XML.
        self.assertEqual(parse('<x>\u03b4</x>'.encode('utf-16')).to_string(),
                         '<x>&#948;</x>')

        # Test setting the inner text and output valid XML.
        e = create('x', '\u03b4'.encode('utf-16'))
        self.assertEqual(e.to_string(encoding='utf-16'), '<x>&#948;</x>')
        # Don't change the encoding until the we convert to an XML string.
        # Allow either little-endian or big-endian byte orderings.
        self.assertTrue(e.text in ['\xff\xfe\xb4\x03', '\xfe\xff\x03\xb4'])
        endianness = LITTLE_ENDIAN
        if e.text == '\xfe\xff\x03\xb4':
            endianness = BIG_ENDIAN
        self.assertTrue(isinstance(e.text, str))
        self.assertTrue(isinstance(e.to_string(encoding='utf-16'), str))
        if endianness == LITTLE_ENDIAN:
            self.assertEqual(
                create('x', '\xff\xfe\xb4\x03').to_string(encoding='utf-16'),
                '<x>&#948;</x>')
        else:
            self.assertEqual(
                create('x', '\xfe\xff\x03\xb4').to_string(encoding='utf-16'),
                '<x>&#948;</x>')

    def testOtherEncodingInTagsAndAttributes(self):
        self.assertEqual(
            parse('<\u03b4elta>test</\u03b4elta>'.encode('utf-16'))._qname,
            '\u03b4elta')
        # Test an element with UTF-16 in the attribute value.
        x = create('x', None)
        x._other_attributes['a'] = '\u03b4'.encode('utf-16')
        self.assertTrue(x.to_string(encoding='UTF-16').startswith('<x a="&#948;"'))


def suite():
    return conf.build_suite([XmlElementTest, UtilityFunctionTest,
                             CharacterEncodingTest])


if __name__ == '__main__':
    unittest.main()

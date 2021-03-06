#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the object filter functions."""

from __future__ import unicode_literals

import unittest

from plaso.lib import errors
from plaso.lib import objectfilter


# pylint: disable=missing-docstring

class DummyObject(object):
  def __init__(self, key, value):
    setattr(self, key, value)


class HashObject(object):
  def __init__(self, hash_value=None):
    self.value = hash_value

  @property
  def md5(self):
    return self.value

  def __eq__(self, y):
    return self.value == y

  def __lt__(self, y):
    return self.value < y


class Dll(object):
  def __init__(self, name, imported_functions=None, exported_functions=None):
    self.name = name
    self._imported_functions = imported_functions or []
    self.num_imported_functions = len(self._imported_functions)
    self.exported_functions = exported_functions or []
    self.num_exported_functions = len(self.exported_functions)

  @property
  def imported_functions(self):
    for fn in self._imported_functions:
      yield fn


class DummyFile(object):
  _FILENAME = 'boot.ini'

  ATTR1 = 'Backup'
  ATTR2 = 'Archive'
  HASH1 = '123abc'
  HASH2 = '456def'

  non_callable_leaf = 'yoda'

  def __init__(self):
    self.non_callable = HashObject(self.HASH1)
    self.non_callable_repeated = [
        DummyObject('desmond', ['brotha', 'brotha']),
        DummyObject('desmond', ['brotha', 'sista'])]
    self.imported_dll1 = Dll('a.dll', ['FindWindow', 'CreateFileA'])
    self.imported_dll2 = Dll('b.dll', ['RegQueryValueEx'])

  @property
  def name(self):
    return self._FILENAME

  @property
  def attributes(self):
    return [self.ATTR1, self.ATTR2]

  @property
  def hash(self):
    return [HashObject(self.HASH1), HashObject(self.HASH2)]

  @property
  def size(self):
    return 10

  @property
  def deferred_values(self):
    for v in ['a', 'b']:
      yield v

  @property
  def novalues(self):
    return []

  @property
  def imported_dlls(self):
    return [self.imported_dll1, self.imported_dll2]

  def Callable(self):
    raise RuntimeError('This can not be called.')

  @property
  def float(self):
    return 123.9823


class LowercaseAttributeFilterImplementation(
    objectfilter.BaseFilterImplementation):
  """Does field name access on the lowercase version of names.

  Useful to only access attributes and properties with Google's python naming
  style.
  """

  FILTERS = {}
  FILTERS.update(objectfilter.BaseFilterImplementation.FILTERS)
  FILTERS.update({
      'ValueExpander': objectfilter.LowercaseAttributeValueExpander})


class ObjectFilterTest(unittest.TestCase):

  def setUp(self):
    """Makes preparations before running an individual test."""
    self.file = DummyFile()
    self.filter_imp = LowercaseAttributeFilterImplementation
    self.value_expander = self.filter_imp.FILTERS['ValueExpander']

  operator_tests = {
      objectfilter.Less: [
          (True, ['size', 1000]),
          (True, ['size', 11]),
          (False, ['size', 10]),
          (False, ['size', 0]),
          (False, ['float', 1.0]),
          (True, ['float', 123.9824])],
      objectfilter.LessEqual: [
          (True, ['size', 1000]),
          (True, ['size', 11]),
          (True, ['size', 10]),
          (False, ['size', 9]),
          (False, ['float', 1.0]),
          (True, ['float', 123.9823])],
      objectfilter.Greater: [
          (True, ['size', 1]),
          (True, ['size', 9.23]),
          (False, ['size', 10]),
          (False, ['size', 1000]),
          (True, ['float', 122]),
          (True, ['float', 1.0])],
      objectfilter.GreaterEqual: [
          (False, ['size', 1000]),
          (False, ['size', 11]),
          (True, ['size', 10]),
          (True, ['size', 0]),
          # Floats work fine too.
          (True, ['float', 122]),
          (True, ['float', 123.9823]),
          # Comparisons works with strings, although it might be a bit silly.
          (True, ['name', 'aoot.ini'])],
      objectfilter.Contains: [
          # Contains works with strings.
          (True, ['name', 'boot.ini']),
          (True, ['name', 'boot']),
          (False, ['name', 'meh']),
          # Works with generators.
          (True, ['imported_dlls.imported_functions', 'FindWindow']),
          # But not with numbers.
          (False, ['size', 12])],
      objectfilter.Equals: [
          (True, ['name', 'boot.ini']),
          (False, ['name', 'foobar']),
          (True, ['float', 123.9823])],
      objectfilter.NotEquals: [
          (False, ['name', 'boot.ini']),
          (True, ['name', 'foobar']),
          (True, ['float', 25])],
      objectfilter.InSet: [
          (True, ['name', ['boot.ini', 'autoexec.bat']]),
          (True, ['name', 'boot.ini']),
          (False, ['name', 'NOPE']),
          # All values of attributes are within these.
          (True, ['attributes', ['Archive', 'Backup', 'Nonexisting']]),
          # Not all values of attributes are within these.
          (False, ['attributes', ['Executable', 'Sparse']])],
      objectfilter.Regexp: [
          (True, ['name', '^boot.ini$']),
          (True, ['name', 'boot.ini']),
          (False, ['name', '^$']),
          (True, ['attributes', 'Archive']),
          # One can regexp numbers if he's inclined to.
          (True, ['size', 0]),
          # But regexp doesn't work with lists or generators for the moment.
          (False, ['imported_dlls.imported_functions', 'FindWindow'])],
      }

  def testBinaryOperators(self):
    for operator, test_data in self.operator_tests.items():
      for test_unit in test_data:
        kwargs = {'arguments': test_unit[1],
                  'value_expander': self.value_expander}
        ops = operator(**kwargs)
        self.assertEqual(
            test_unit[0], ops.Matches(self.file),
            'test case {0!s} failed'.format(test_unit))
        if hasattr(ops, 'FlipBool'):
          ops.FlipBool()
          self.assertEqual(not test_unit[0], ops.Matches(self.file))

  def testExpand(self):
    # Case insensitivity.
    values_lowercase = self.value_expander().Expand(self.file, 'size')
    values_uppercase = self.value_expander().Expand(self.file, 'Size')
    self.assertListEqual(list(values_lowercase), list(values_uppercase))

    # Existing, non-repeated, leaf is a value.
    values = self.value_expander().Expand(self.file, 'size')
    self.assertListEqual(list(values), [10])

    # Existing, non-repeated, leaf is iterable.
    values = self.value_expander().Expand(self.file, 'attributes')
    self.assertListEqual(list(values), [[DummyFile.ATTR1, DummyFile.ATTR2]])

    # Existing, repeated, leaf is value.
    values = self.value_expander().Expand(self.file, 'hash.md5')
    self.assertListEqual(list(values), [DummyFile.HASH1, DummyFile.HASH2])

    # Existing, repeated, leaf is iterable.
    values = self.value_expander().Expand(
        self.file, 'non_callable_repeated.desmond')
    self.assertListEqual(
        list(values), [['brotha', 'brotha'], ['brotha', 'sista']])

    # Now with an iterator.
    values = self.value_expander().Expand(self.file, 'deferred_values')
    self.assertListEqual([list(value) for value in values], [['a', 'b']])

    # Iterator > generator.
    values = self.value_expander().Expand(
        self.file, 'imported_dlls.imported_functions')
    expected = [['FindWindow', 'CreateFileA'], ['RegQueryValueEx']]
    self.assertListEqual([list(value) for value in values], expected)

    # Non-existing first path.
    values = self.value_expander().Expand(self.file, 'nonexistant')
    self.assertListEqual(list(values), [])

    # Non-existing in the middle.
    values = self.value_expander().Expand(self.file, 'hash.mink.boo')
    self.assertListEqual(list(values), [])

    # Non-existing as a leaf.
    values = self.value_expander().Expand(self.file, 'hash.mink')
    self.assertListEqual(list(values), [])

    # Non-callable leaf.
    values = self.value_expander().Expand(self.file, 'non_callable_leaf')
    self.assertListEqual(list(values), [DummyFile.non_callable_leaf])

    # callable.
    values = self.value_expander().Expand(self.file, 'Callable')
    self.assertListEqual(list(values), [])

    # leaf under a callable. Will return nothing.
    values = self.value_expander().Expand(self.file, 'Callable.a')
    self.assertListEqual(list(values), [])

  def testGenericBinaryOperator(self):
    class TestBinaryOperator(objectfilter.GenericBinaryOperator):
      values = list()

      def Operation(self, x, _):
        return self.values.append(x)

    # Test a common binary operator.
    tbo = TestBinaryOperator(
        arguments=['whatever', 0], value_expander=self.value_expander)
    self.assertEqual(tbo.right_operand, 0)
    self.assertEqual(tbo.args[0], 'whatever')
    tbo.Matches(DummyObject('whatever', 'id'))
    tbo.Matches(DummyObject('whatever', 'id2'))
    tbo.Matches(DummyObject('whatever', 'bg'))
    tbo.Matches(DummyObject('whatever', 'bg2'))
    self.assertListEqual(tbo.values, ['id', 'id2', 'bg', 'bg2'])

  def testContext(self):
    self.assertRaises(
        objectfilter.InvalidNumberOfOperands, objectfilter.Context,
        arguments=['context'], value_expander=self.value_expander)

    self.assertRaises(
        objectfilter.InvalidNumberOfOperands, objectfilter.Context,
        arguments=[
            'context', objectfilter.Equals(
                arguments=['path', 'value'],
                value_expander=self.value_expander),
            objectfilter.Equals(
                arguments=['another_path', 'value'],
                value_expander=self.value_expander)],
        value_expander=self.value_expander)

    # One imported_dll imports 2 functions AND one imported_dll imports
    # function RegQueryValueEx.
    arguments = [
        objectfilter.Equals(
            arguments=['imported_dlls.num_imported_functions', 1],
            value_expander=self.value_expander),
        objectfilter.Contains(
            arguments=['imported_dlls.imported_functions',
                       'RegQueryValueEx'],
            value_expander=self.value_expander)]
    condition = objectfilter.AndFilter(arguments=arguments)
    # Without context, it matches because both filters match separately.
    self.assertEqual(True, condition.Matches(self.file))

    arguments = [
        objectfilter.Equals(
            arguments=['num_imported_functions', 2],
            value_expander=self.value_expander),
        objectfilter.Contains(
            arguments=['imported_functions', 'RegQueryValueEx'],
            value_expander=self.value_expander)]
    condition = objectfilter.AndFilter(arguments=arguments)
    # The same DLL imports 2 functions AND one of these is RegQueryValueEx.
    context = objectfilter.Context(arguments=['imported_dlls', condition],
                                   value_expander=self.value_expander)
    # With context, it doesn't match because both don't match in the same dll.
    self.assertEqual(False, context.Matches(self.file))

    # One imported_dll imports only 1 function AND one imported_dll imports
    # function RegQueryValueEx.
    condition = objectfilter.AndFilter(arguments=[
        objectfilter.Equals(
            arguments=['num_imported_functions', 1],
            value_expander=self.value_expander),
        objectfilter.Contains(
            arguments=['imported_functions', 'RegQueryValueEx'],
            value_expander=self.value_expander)])
    # The same DLL imports 1 function AND it's RegQueryValueEx.
    context = objectfilter.Context(['imported_dlls', condition],
                                   value_expander=self.value_expander)
    self.assertEqual(True, context.Matches(self.file))

    # Now test the context with a straight query.
    query = '\n'.join([
        '@imported_dlls',
        '(',
        '  imported_functions contains "RegQueryValueEx"',
        '  AND num_imported_functions == 1',
        ')'])

    filter_ = objectfilter.Parser(query).Parse()
    filter_ = filter_.Compile(self.filter_imp)
    self.assertEqual(True, filter_.Matches(self.file))

  def testRegexpRaises(self):
    with self.assertRaises(ValueError):
      objectfilter.Regexp(
          arguments=['name', 'I [dont compile'],
          value_expander=self.value_expander)

  def testEscaping(self):
    parser = objectfilter.Parser(r'a is "\n"').Parse()
    self.assertEqual(parser.args[0], '\n')
    # Invalid escape sequence.
    parser = objectfilter.Parser(r'a is "\z"')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Can escape the backslash.
    parser = objectfilter.Parser(r'a is "\\"').Parse()
    self.assertEqual(parser.args[0], '\\')

    # Test hexadecimal escaping.

    # This fails as it's not really a hex escaped string.
    parser = objectfilter.Parser(r'a is "\xJZ"')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Instead, this is what one should write.
    parser = objectfilter.Parser(r'a is "\\xJZ"').Parse()
    self.assertEqual(parser.args[0], r'\xJZ')
    # Standard hex-escape.
    parser = objectfilter.Parser('a is "\x41\x41\x41"').Parse()
    self.assertEqual(parser.args[0], 'AAA')
    # Hex-escape + a character.
    parser = objectfilter.Parser('a is "\x414"').Parse()
    self.assertEqual(parser.args[0], 'A4')
    # How to include r'\x41'.
    parser = objectfilter.Parser('a is "\\x41"').Parse()
    self.assertEqual(parser.args[0], '\x41')

  def testParse(self):
    # Arguments are either int, float or quoted string.
    objectfilter.Parser('attribute == 1').Parse()
    objectfilter.Parser('attribute == 0x10').Parse()
    parser = objectfilter.Parser('attribute == 1a')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    objectfilter.Parser('attribute == 1.2').Parse()
    objectfilter.Parser('attribute == \'bla\'').Parse()
    objectfilter.Parser('attribute == "bla"').Parse()
    parser = objectfilter.Parser('something == red')
    self.assertRaises(errors.ParseError, parser.Parse)

    # Can't start with AND.
    parser = objectfilter.Parser('and something is \'Blue\'')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Test negative filters.
    parser = objectfilter.Parser('attribute not == \'dancer\'')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    parser = objectfilter.Parser('attribute == not \'dancer\'')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    parser = objectfilter.Parser('attribute not not equals \'dancer\'')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    parser = objectfilter.Parser('attribute not > 23')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Need to close braces.
    objectfilter.Parser('(a is 3)').Parse()
    parser = objectfilter.Parser('(a is 3')
    self.assertRaises(errors.ParseError, parser.Parse)
    # Need to open braces to close them.
    parser = objectfilter.Parser('a is 3)')
    self.assertRaises(errors.ParseError, parser.Parse)

    # Context Operator alone is not accepted.
    parser = objectfilter.Parser('@attributes')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Accepted only with braces.
    objectfilter.Parser('@attributes( name is \'adrien\')').Parse()
    # Not without them.
    parser = objectfilter.Parser('@attributes name is \'adrien\'')
    with self.assertRaises(errors.ParseError):
      parser.Parse()

    # Can nest context operators.
    query = '@imported_dlls( @imported_function( name is \'OpenFileA\'))'
    objectfilter.Parser(query).Parse()
    # Can nest context operators and mix braces without it messing up.
    query = '@imported_dlls( @imported_function( name is \'OpenFileA\'))'
    parser = objectfilter.Parser(query).Parse()
    query = '\n'.join([
        '@imported_dlls',
        '(',
        '  @imported_function',
        '  (',
        '    name is "OpenFileA" and ordinal == 12',
        '  )',
        ')'])

    parser = objectfilter.Parser(query).Parse()
    # Mix context and binary operators.
    query = '\n'.join([
        '@imported_dlls',
        '(',
        '  @imported_function',
        '  (',
        '    name is "OpenFileA"',
        '  ) AND num_functions == 2',
        ')'])

    parser = objectfilter.Parser(query).Parse()
    # Also on the right.
    query = '\n'.join([
        '@imported_dlls',
        '(',
        '  num_functions == 2 AND',
        '  @imported_function',
        '  (',
        '    name is "OpenFileA"',
        '  )',
        ')'])

  # Altogether.
  # There's an imported dll that imports OpenFileA AND
  # an imported DLL matching advapi32.dll that imports RegQueryValueExA AND
  # and it exports a symbol called 'inject'.
  query = '\n'.join([
      '@imported_dlls( @imported_function ( name is "OpenFileA" ) )',
      'AND',
      '@imported_dlls (',
      '  name regexp "(?i)advapi32.dll"',
      '  AND @imported_function ( name is "RegQueryValueEx" )',
      ')',
      'AND @exported_symbols(name is "inject")'])

  def testCompile(self):
    obj = DummyObject('something', 'Blue')
    parser = objectfilter.Parser('something == \'Blue\'').Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), True)
    parser = objectfilter.Parser('something == \'Red\'').Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), False)
    parser = objectfilter.Parser('something == "Red"').Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), False)
    obj = DummyObject('size', 4)
    parser = objectfilter.Parser('size < 3').Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), False)
    parser = objectfilter.Parser('size == 4').Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), True)
    query = 'something is \'Blue\' and size not contains 3'
    parser = objectfilter.Parser(query).Parse()
    filter_ = parser.Compile(self.filter_imp)
    self.assertEqual(filter_.Matches(obj), False)


if __name__ == '__main__':
  unittest.main()

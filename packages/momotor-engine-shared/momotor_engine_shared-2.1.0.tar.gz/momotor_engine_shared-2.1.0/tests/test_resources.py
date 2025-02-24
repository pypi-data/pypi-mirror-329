from contextlib import contextmanager

import pytest

from momotor.shared.resources import NoMatch, ResourceGroup, Resources, \
    split_resources
from momotor.shared.resources.const import NEUTRAL, STRONG, STRONGEST, WEAK, \
    WEAKEST
from momotor.shared.resources.item import ResourceItem, split_items
from momotor.shared.resources.tag import Tag


@pytest.mark.parametrize(['l', 'r'], [
    [WEAKEST, WEAK],
    [WEAK, NEUTRAL],
    [NEUTRAL, STRONG],
    [STRONG, STRONGEST]
])
def test_constants(l, r):
    assert l > r


@contextmanager
def execute_match(expected):
    def assert_(value):
        assert value == expected

    try:
        yield assert_
    except Exception as e:
        if isinstance(expected, type) and issubclass(expected, Exception):
            assert isinstance(e, expected)
        else:
            raise


@pytest.mark.parametrize(['req1', 'exc1', 'req2', 'exc2', 'expected'], [
    pytest.param(True, False, True,  False,  STRONGEST, id='req-req'),
    pytest.param(True, False, False, False,  STRONG,    id='req-opt'),
    pytest.param(True, False, False, True,   NoMatch,   id='req-exc'),

    pytest.param(False, False, True,  False, WEAK,     id='opt-req'),
    pytest.param(False, False, False, False, WEAKEST,  id='opt-opt'),
    pytest.param(False, False, False, True,  NoMatch,  id='opt-exc'),

    pytest.param(False, True,  True,  False, NoMatch,  id='exc-req'),
    pytest.param(False, True,  False, False, NoMatch,  id='exc-opt'),
    pytest.param(False, True,  False, True,  None,     id='exc-exc'),
])
def test_resource_item_compare_flags(req1, exc1, req2, exc2, expected):
    with execute_match(expected) as assert_:
        assert_(
            ResourceItem('value', req1, exc1).compare(ResourceItem('value', req2, exc2))
        )


@pytest.mark.parametrize(['req', 'exc', 'expected'], [
    pytest.param(True, False,  NoMatch, id='req'),
    pytest.param(False, False, None,    id='opt'),
    pytest.param(False, True,  None,    id='exc'),
])
def test_resource_item_compare_missing(req, exc, expected):
    with execute_match(expected) as assert_:
        assert_(
            ResourceItem.compare_missing(ResourceItem('value', req, exc))
        )


def test_resource_item_invalid_flags():
    with pytest.raises(ValueError):
        ResourceItem('value', True, True)


@pytest.mark.parametrize(['name', 'value', 'required', 'excluded'], [
    pytest.param('tag',  'tag', True, False),
    pytest.param('?tag', 'tag', False, False),
    pytest.param('~tag', 'tag', False, True),
])
def test_tag_create(name, value, required, excluded):
    tags = list(ResourceItem.create(name))
    assert len(tags) == 1
    tag = tags[0]
    assert isinstance(tag, Tag)
    assert tag.value == value
    assert tag.required == required
    assert tag.excluded == excluded


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                     set()),
    ([''],                   set()),
    (['tag'],                {'tag'}),
    (['tag1', 'tag2'],       {'tag1', 'tag2'}),
    (['tag1', 'tag2 '],      {'tag1', 'tag2'}),
    (['tag1,tag2'],          {'tag1', 'tag2'}),
    (['tag1, tag2'],         {'tag1', 'tag2'}),
    (['tag1, tag2 '],        {'tag1', 'tag2'}),
    (['tag1, tag2', 'tag2'], {'tag1', 'tag2'}),
])
def test_resource_item_set_creation(values, expected):
    items = set(str(item) for item in ResourceItem.create(values))
    assert items == expected


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                     []),
    (['a', 'b'],             ['a', 'b']),
    (['b', 'a'],             ['a', 'b']),
    (['a', '?a', '~a'],      ['~a', 'a', '?a']),
    (['b', '?a', '~a', 'a'], ['~a', 'a', '?a', 'b']),
])
def test_resource_item_ordering(values, expected):
    items = [str(item) for item in sorted(ResourceItem.create(values))]
    assert items == expected


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                    ''),
    (['a'],                 'a'),
    (['a', 'a'],            'a'),
    (['a,b'],               'a,b'),
    (['a', 'b'],            'a,b'),
    (['b', 'a'],            'b,a'),
    (['a,b', 'a'],          'a,b'),
    (['b,a', 'a'],          'b,a'),
    (['a,b', 'a,c'],        'a,b,c'),
    (['a,b', 'b,c', 'c,d'], 'a,b,c,d'),
    (['?a', '~a'],          '?a,~a'),
])
def test_resource_group_union(values, expected):
    groups = [
        ResourceGroup.create(value)
        for value in values
    ]
    result = ResourceGroup.union(*groups)
    assert result.as_str() == expected


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                    ''),
    (['a'],                 'a'),
    (['a', 'a'],            ''),
    (['a,b'],               'a,b'),
    (['a', 'b'],            'a'),
    (['b', 'a'],            'b'),
    (['a,b', 'a'],          'b'),
    (['b,a', 'a'],          'b'),
    (['a,b', 'a,c'],        'b'),
    (['a,b', 'b,c', 'c,d'], 'a'),
    (['?a', '~a'],          '?a'),
])
def test_resource_group_difference(values, expected):
    groups = [
        ResourceGroup.create(value)
        for value in values
    ]
    result = ResourceGroup.difference(*groups)
    assert result.as_str() == expected


@pytest.mark.parametrize(['task', 'worker', 'expected'], [
    # Test the matching table as described in the documentation
    pytest.param('',          '',            None),
    pytest.param('tag1',      '',            NoMatch),
    pytest.param('?tag1',     '',            None),
    pytest.param('~tag1',     '',            None),

    pytest.param('',          'tag1',        NoMatch),
    pytest.param('tag1',      'tag1',        STRONGEST),
    pytest.param('?tag1',     'tag1',        WEAK),
    pytest.param('~tag1',     'tag1',        NoMatch),

    pytest.param('',          '?tag1',       None),
    pytest.param('tag1',      '?tag1',       STRONG),
    pytest.param('?tag1',     '?tag1',       WEAKEST),
    pytest.param('~tag1',     '?tag1',       NoMatch),

    pytest.param('',          '~tag1',       None),
    pytest.param('tag1',      '~tag1',       NoMatch),
    pytest.param('?tag1',     '~tag1',       NoMatch),
    pytest.param('~tag1',     '~tag1',       None),

    # Test combinations
    pytest.param('tag1',      'tag2',        NoMatch),      # tag1: NoMatch    tag2: NoMatch
    pytest.param('tag1',      'tag1,tag2',   NoMatch),      # tag1: STRONGEST  tag2: NoMatch
    pytest.param('tag1,tag2', 'tag1',        NoMatch),      # tag1: STRONGEST  tag2: NoMatch
    pytest.param('tag1,tag2', 'tag1,tag2',   STRONGEST),    # tag1: STRONGEST  tag2: STRONGEST

    pytest.param('tag1,?tag2', 'tag1',       STRONGEST),    # tag1: STRONGEST  tag2: None
    pytest.param('tag1',       'tag1,?tag2', STRONGEST),    # tag1: STRONGEST  tag2: None
    pytest.param('?tag1,tag2', 'tag1',       NoMatch),      # tag1: WEAK       tag2: NoMatch
    pytest.param('tag1',       '?tag1,tag2', NoMatch),      # tag1: STRONG     tag2: NoMatch

    pytest.param('tag1,~tag2', 'tag1',       STRONGEST),    # tag1: STRONGEST  tag2: None
    pytest.param('tag1',       'tag1,~tag2', STRONGEST),    # tag1: STRONGEST  tag2: None
    pytest.param('~tag1,tag2', 'tag1',       NoMatch),      # tag1: NoMatch    tag2: NoMatch
    pytest.param('tag1',       '~tag1,tag2', NoMatch),      # tag1: NoMatch    tag2: NoMatch
])
def test_resource_group_compare(task, worker, expected):
    task_group = ResourceGroup.create(task)
    worker_group = ResourceGroup.create(worker) if worker is not None else None
    with execute_match(expected) as assert_:
        assert_(
            task_group.match(worker_group)
        )


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                     ''),
    (['a: 1,2'],             'a: 1,2'),
    (['a: 1,2', 'b: 3,4'],   'a: 1,2; b: 3,4'),
    (['a: 1,2', 'a: 3,4'],   'a: 1,2,3,4'),
    (['a: 1,2', 'a: 2,3'],   'a: 1,2,3'),
    (['a: 1,2', 'a: 1,2,3'], 'a: 1,2,3'),
])
def test_resources_union(values, expected):
    resources = [
        Resources.from_string(value)
        for value in values
    ]
    result = Resources.union(*resources)
    assert result.as_str() == expected


@pytest.mark.parametrize(['values', 'expected'], [
    ([],                     ''),
    (['a: 1,2'],             'a: 1,2'),
    (['a: 1,2', 'b: 3,4'],   'a: 1,2'),
    (['a: 1,2', 'a: 3,4'],   'a: 1,2'),
    (['a: 1,2', 'a: 2,3'],   'a: 1'),
    (['a: 1,2', 'a: 1,2,3'], ''),
])
def test_resources_difference(values, expected):
    resources = [
        Resources.from_string(value)
        for value in values
    ]
    result = Resources.difference(*resources)
    assert result.as_str() == expected


@pytest.mark.parametrize(['worker', 'task', 'expected'], [
    [  # 0
        {},
        {},
        NEUTRAL
    ], [  # 1
        {'group1': ['tag1']},
        {},
        NoMatch
    ], [  # 2
        {'group1': ['?tag1']},
        {},
        NEUTRAL
    ], [  # 3
        {},
        {'group1': ['tag1']},
        NoMatch
    ], [  # 4
        {},
        {'group1': ['?tag1']},
        NEUTRAL
    ], [  # 5
        {'group1': ['tag1']},
        {'group1': ['tag1']},
        STRONGEST
    ], [  # 6
        {'group1': ['?tag1']},
        {'group1': ['tag1']},
        STRONG
    ], [  # 7
        {'group1': ['~tag1']},
        {'group1': ['tag1']},
        NoMatch
    ], [  # 8
        {'group1': ['tag2']},
        {'group1': ['tag1']},
        NoMatch
    ], [  # 9
        {'group2': ['tag1']},
        {'group1': ['tag1']},
        NoMatch
    ], [  # 10
        {'group1': ['tag1'], 'group2': ['?tag1']},
        {'group1': ['tag1'], 'group2': ['tag1']},
        STRONG
    ], [  # 11
        {'group1': ['tag1'], 'group2': ['~tag1']},
        {'group1': ['tag1'], 'group2': ['tag1']},
        NoMatch
    ], [  # 12
        {'group1': ['tag2'], 'group2': ['tag1']},
        {'group1': ['tag1'], 'group2': ['tag2']},
        NoMatch
    ], [  # 13
        {'group1': ['tag1']},
        {'group1': ['tag1'], 'group2': ['tag2']},
        NoMatch
    ], [  # 14
        {'group1': ['tag1'], 'group2': ['tag2']},
        {'group1': ['tag1']},
        NoMatch
    ], [  # 15
        {'group1': ['tag1']},
        {'group1': ['tag1'], 'group2': ['?tag2']},
        NEUTRAL
    ], [  # 16
        {'group1': ['tag1'], 'group2': ['?tag2']},
        {'group1': ['tag1']},
        NEUTRAL
    ], [  # 17
        {'group1': ['tag1'], 'group2': ['tag2']},
        {'group1': ['tag1'], 'group2': ['?tag2']},
        WEAK
    ], [  # 18
        {'group1': ['tag1'], 'group2': ['?tag2']},
        {'group1': ['tag1'], 'group2': ['tag2']},
        STRONG
    ], [  # 19
        {'group1': ['tag1'], 'group2': ['tag2a']},
        {'group1': ['tag1'], 'group2': ['tag2b']},
        NoMatch
    ], [  # 20
        {'group1': ['tag1'], 'group2': ['tag2a']},
        {'group1': ['tag1'], 'group2': ['?tag2b']},
        NoMatch
    ], [  # 21
        {'group1': ['tag1'], 'group2': ['?tag2a']},
        {'group1': ['tag1'], 'group2': ['tag2b']},
        NoMatch
    ], [  # 22
        {'group1': ['tag1'], 'group2': ['?tag2a']},
        {'group1': ['tag1'], 'group2': ['?tag2b']},
        NEUTRAL
    ],
])
def test_resource(worker, task, expected):
    worker_resource = Resources.from_dict(worker)
    task_resource = Resources.from_dict(task)
    with execute_match(expected) as assert_:
        assert_(
            task_resource.match(worker_resource)
        )


EXAMPLE_PROG_LANG_WORKER = 'language: ?java, ?python; java: ?8, ?11, ?12, ?13; python: ?3.6, ?3.7'


@pytest.mark.parametrize(['worker', 'task', 'expected'], [
    [
        EXAMPLE_PROG_LANG_WORKER,
        'language: java; java: 12',
        NEUTRAL
    ],
    [
        EXAMPLE_PROG_LANG_WORKER,
        'language: java; java: 14',
        NoMatch
    ],
    [
        EXAMPLE_PROG_LANG_WORKER,
        'language: java; java: ?14',
        NEUTRAL
    ],
    [
        EXAMPLE_PROG_LANG_WORKER,
        'arch: x86',
        NoMatch
    ],
    [
        EXAMPLE_PROG_LANG_WORKER,
        'arch: ?x86',
        NEUTRAL
    ],
    [
        EXAMPLE_PROG_LANG_WORKER,
        'arch: ~x86',
        NEUTRAL
    ],
])
def test_resource_examples(worker, task, expected):
    worker_resource = Resources.from_string(worker)
    task_resource = Resources.from_string(task)
    with execute_match(expected) as assert_:
        assert_(
            task_resource.match(worker_resource)
        )


@pytest.mark.parametrize(['resource_str'], [
    [r'key:tag1,tag2,tag3'],
    [r'"key:":tag1,tag2,tag3'],
    [r'key\::tag1,tag2,tag3'],
    [r'key:"xxx,yyy,zzz"'],
    [r'key:xxx\,yyy\,zzz'],
    [r'key:"tag1:tag2:tag3"'],
    [r'key1:tag1,tag2,tag3;key2:tag4,tag5,tag6'],
    [r'key1:tag1,tag2,"xxx;yyy:zzz",tag5,tag6'],
    ['"\'"\'"\'\\\'\\":tag1'],  # The group name is '"'" (literally, these 4 quotes)
])
def test_string_conversion(resource_str):
    """ Test that string conversion is idempotent
    """
    input_resource = Resources.from_string(resource_str)
    converted_resource_str = input_resource.as_str()
    converted_resource = Resources.from_string(converted_resource_str)
    assert list(input_resource.as_tuples()) == list(converted_resource.as_tuples())


@pytest.mark.parametrize(['resources', 'expected'], [
    pytest.param('key:', [('key', '')]),
    pytest.param('key:value', [('key', 'value')]),
    pytest.param('"key":value', [('key', 'value')]),
    pytest.param('"key:":value', [('key:', 'value')]),
    pytest.param('"key;":value', [('key;', 'value')]),
    pytest.param('key: " value "', [('key', '" value "')]),
    pytest.param('key:value;key2:value2', [('key', 'value'), ('key2', 'value2')]),
    pytest.param('key:value; key2:value2', [('key', 'value'), ('key2', 'value2')]),
    pytest.param('key:"value;1"; key2:value2', [('key', '"value;1"'), ('key2', 'value2')]),
    pytest.param('key>value,value', [('key', '>value,value')]),
    pytest.param('key-with-dashes: value', [('key-with-dashes', 'value')]),
    pytest.param('key.with.dots: value', [('key.with.dots', 'value')]),
    pytest.param('key_with_underscores: value', [('key_with_underscores', 'value')]),
    pytest.param('"key:with:colon" : value', [('key:with:colon', 'value')]),
    pytest.param('key with spaces : value', [('key with spaces', 'value')]),
    pytest.param('"key with spaces ": value', [('key with spaces ', 'value')]),
])
def test_split_resources(resources, expected):
    assert list(split_resources(resources)) == expected


@pytest.mark.parametrize(['items', 'expected'], [
    pytest.param('', ['']),
    pytest.param(',', ['', '']),
    pytest.param('tag', ['tag']),
    pytest.param('tag, tag', ['tag', 'tag']),
    pytest.param('spaced tag', ['spaced tag']),
    pytest.param('comma,tag', ['comma', 'tag']),
    pytest.param('"quoted,comma,tag"', ['quoted,comma,tag']),
    pytest.param('"quoted\\"with escape"', ['quoted"with escape']),
    pytest.param('quoted "with spaces "', ['quoted with spaces ']),
    pytest.param('\\"quoted\\"', ['"quoted"']),
])
def test_split_items(items, expected):
    assert list(split_items(items)) == expected


@pytest.mark.parametrize(['resource', 'expected'], [
    pytest.param('key:value', {'key': {'value'}}),
    pytest.param('key:value1,value2', {'key': {'value1', 'value2'}}),
    pytest.param('key:value1, value2', {'key': {'value1', 'value2'}}),
    pytest.param('key: "quoted"', {'key': {'quoted'}}),
    pytest.param('key: ~"quoted"', {'key': {'~quoted'}}),
    pytest.param('key: "~quoted"', {'key': {'~quoted'}}),
    pytest.param("key: ' quoted with spaces '", {'key': {' quoted with spaces '}}),
    pytest.param("key: 'quoted, with comma'", {'key': {'quoted, with comma'}}),
    pytest.param('key: "value with spaces", "another value"', {'key': {'value with spaces', 'another value'}}),
    pytest.param('key : value1 , value2  ', {'key': {'value1', 'value2'}}),
    pytest.param('key:>value1,<value2', {'key': {'>value1', '<value2'}}),
    pytest.param('key>value1,<value2', {'key': {'>value1', '<value2'}}),
    pytest.param('key >value1, <value2', {'key': {'>value1', '<value2'}}),
    pytest.param('key :>value1, <value2', {'key': {'>value1', '<value2'}}),
    pytest.param('key : >value1, <value2', {'key': {'>value1', '<value2'}}),
    pytest.param('key : >=value1, <value2', {'key': {'>=value1', '<value2'}}),
    pytest.param('key1:value1,value2; key2:value3', {'key1': {'value1', 'value2'}, 'key2': {'value3'}}),
    pytest.param('key1:value1,value2\nkey2:value3', {'key1': {'value1', 'value2'}, 'key2': {'value3'}}),
    pytest.param('key: "value:123"', {'key': {'value:123'}}),

    # Examples from the documentation
    pytest.param('lang: python, java', {'lang': {'python', 'java'}}),
    pytest.param('memory < 1 GiB', {'memory': {'< 1 GiB'}}),
    pytest.param('version <3, >=5', {'version': {'<3', '>=5'}}),
    pytest.param('test case: "one; two, or more"', {'test case': {'one; two, or more'}}),
    pytest.param('one: 1; two: 2', {'one': {'1'}, 'two': {'2'}}),
])
def test_parse_resource_string(resource, expected):
    resources = Resources.from_string(resource)
    assert dict((key, set(items)) for key, items in resources.as_tuples()) == expected


def test_resource_colon():
    with pytest.raises(ValueError):
        Resources.from_string('key: value:')


def test_ordering_is_retained():
    resources = Resources.from_string('a:5,a,4,b,3,c,2,d,1;z:;1:;y:')
    assert tuple(resources.as_tuples()) == (
        ('a', ('5', 'a', '4', 'b', '3', 'c', '2', 'd', '1',)),
        ('z', tuple()),
        ('1', tuple()),
        ('y', tuple()),
    )

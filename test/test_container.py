def test_container(tracer):
    a = b = 1
    c = 2
    e = 0

    tracer.init()

    d = [a, b]  # BUILD_LIST
    d = (a, b)  # BUILD_TUPLE
    d = {a, b}  # BUILD_SET
    d = {a: b}  # BUILD_MAP
    d = {1: a, 2: b}  # BUILD_CONST_KEY_MAP
    d[a] = c  # STORE_SUBSCR
    del d[a]  # DELETE_SUBSCR
    d = [a, b, c][e:c]  # BUILD_SLICE, [1, 1, 2][0:2]
    d = [b, b, c][e:c:a]  # BUILD_SLICE, [1, 1, 2][0:2:1]

    tracer.register()

    assert tracer.logger.changes == [
        {"target": "d", "value": [1, 1], "sources": {"a", "b"}},
        {"target": "d", "value": (1, 1), "sources": {"a", "b"}},
        {"target": "d", "value": {1}, "sources": {"a", "b"}},
        {"target": "d", "value": {1: 1}, "sources": {"a", "b"}},
        {"target": "d", "value": {1: 1, 2: 1}, "sources": {"a", "b"}},
        {"target": "d", "value": {1: 2, 2: 1}, "sources": {"a", "c"}},
        {"target": "d", "value": {2: 1}, "sources": {"a"}},
        {"target": "d", "value": [1, 1], "sources": {"a", "b", "c", "e"}},
        {"target": "d", "value": [1, 1], "sources": {"a", "b", "c", "e"}},
    ]

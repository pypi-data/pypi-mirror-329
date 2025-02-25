def test_nogarbage_fixture(testdir):
    testdir.makepyfile("""
        def test_fail(nogarbage):
            assert False

        def test_pass(nogarbage):
            pass

        def test_except(nogarbage):
            try:
                assert False
            except AssertionError:
                pass

        def test_circular(nogarbage):
            l1 = []
            l2 = [l1]
            l1.append(l2)

        def test_collect(nogarbage):
            import gc
            gc.collect()
    """)

    result = testdir.runpytest(
        '-v'
    )

    result.stdout.fnmatch_lines([
        '*::test_fail FAIL*',
        '*::test_pass PASS*',
        '*::test_except PASS*',
        '*::test_circular ERROR*',
        '*::test_collect ERROR*',
    ])

    assert result.ret != 0

import pikzie
from test.utils import Assertions, collect_fault_info

fixture_dir = "test/fixtures/data_driven_test"
pattern = fixture_dir + "/test_*.py"

def test_assertions():
    prefix = 'test.fixtures.data_driven_test.test_assertions'
    assert_result(False, 3, 2, 1, 0, 0, 0,
                  [['F',
                    prefix + '.test_assert_equal (fail)',
                    "expected: <'abc'>\n"
                    " but was: <'def'>",
                    None]],
                  test_case_names=["/test_assertions/"])

def assert_result(succeeded, n_tests, n_assertions, n_failures,
                  n_errors, n_pendings, n_notifications, fault_info,
                  **kw_args):
    context = pikzie.TestRunnerContext()
    _kw_args = {"pattern": pattern, "priority_mode": False}
    for name in kw_args:
        _kw_args[name] = kw_args[name]
    # _kw_args.update(**kw_args) # require Python >= 2.4
    loader = pikzie.TestLoader(**_kw_args)
    test_suite = loader.create_test_suite()
    test_suite.run(context)

    assert_equal(Assertions.RegexpMatchResult(succeeded,
                                              (n_tests,
                                               n_assertions,
                                               n_failures,
                                               n_errors,
                                               n_pendings,
                                               n_notifications),
                                              fault_info),
                 Assertions.RegexpMatchResult(context.succeeded,
                                              (context.n_tests,
                                               context.n_assertions,
                                               context.n_failures,
                                               context.n_errors,
                                               context.n_pendings,
                                               context.n_notifications),
                                              map(collect_fault_info,
                                                  context.faults)))

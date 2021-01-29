"""Contains tests for the brain module"""
import sys
sys.path.insert(0, '.')

from gauss.brain import do_integration
TEST_PROBLEMS = open('tests/TEST_PROBLEMS.txt', 'r').readlines()


def test_integration():
    """Tests the integration for various inputs"""
    result = ''

    for problem in TEST_PROBLEMS:
        try:
            result += str(do_integration(problem)) + '\n'
        except Exception as exc:
            print(problem, str(exc))
            print(sys.exc_info()[2].tb_frame.f_code.co_filename)

    with open('tests/TEST_RESULT.txt', 'w') as f:
        assert result == f.read()


if __name__ == '__main__':
    test_integration()

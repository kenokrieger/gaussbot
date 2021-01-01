"""Contains tests for the brain module"""
import gauss.brain
import sys

TEST_PROBLEMS = open('TEST_PROBLEMS.txt', 'r').readlines()


def test_integration():
    """Tests the integration for various inputs"""
    result = ''

    for problem in TEST_PROBLEMS:
        try:
            result += str(gauss.brain.do_integration(problem)) + '\n'
        except Exception as exc:
            print(problem, str(exc))
            print(sys.exc_info()[2].tb_frame.f_code.co_filename)

    with open('TEST_RESULT.txt', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    test_integration()
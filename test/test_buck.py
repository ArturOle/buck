from buck import buck_aws


def test_check_credentials_correct(mocker):
    session_mock = mocker.patch("buck.buck_aws.boto3.Session")
    mocker.patch("os.getenv", return_value="key")

    @buck_aws.check_credentials
    def test_function(_session):
        pass

    test_function()
    session_mock.assert_called_once_with(
        aws_access_key_id="key",
        aws_secret_access_key="key"
    )


def test_check_credentials_incorrect(mocker):
    mocker.patch("os.getenv", return_value=None)

    @buck_aws.check_credentials
    def test_function():
        pass

    try:
        test_function()
    except buck_aws.CredentialsError as e:
        assert str(e) == "AWS_SECRET_ACCESS_KEY not set"
    else:
        assert False

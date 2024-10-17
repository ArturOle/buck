from buck import buck_aws


# Credentials check tests

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


# boto tests


def test_list_all_in_bucket_correct(mocker):
    s3_mock = mocker.MagicMock()
    s3_mock.list_objects_v2.return_value = {
        "Contents": [{"Key": "file1"}, {"Key": "file2"}]
    }
    mocker.patch("buck.buck_aws.boto3.Session.client", return_value=s3_mock)

    result = buck_aws.list_all_in_bucket()
    assert result == ["file1", "file2"]

    s3_mock.list_objects_v2.assert_called_once_with(
        Bucket="developer-task2",
        Prefix="TIE-sa"
    )


def test_list_all_in_bucket_no_files(mocker):
    s3_mock = mocker.MagicMock()
    s3_mock.list_objects_v2.return_value = {}
    mocker.patch("buck.buck_aws.boto3.Session.client", return_value=s3_mock)

    result = buck_aws.list_all_in_bucket()
    assert result is None

import pytest
from init_data import InitData
from init_data.main import InvalidInitDataError


single_encoded_init_data = {
    "data": "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A279058397%2C%22first_name%22%3A%22Vladislav%22%2C%22last_name%22%3A%22Kibenko%22%2C%22username%22%3A%22vdkfrost%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%7D&auth_date=1662771648&hash=c501b71e775f74ce10e377dea85a7ea24ecd640b223ea86dfe453e0eaed2e2b2",
    "bot_token": "5768337691:AAH5YkoiEuPk8-FZa32hStHTqXiLPtAEhx8"
}

double_encoded_init_data = {
    "data": "user%3D%257B%2522id%2522%253A2200633365%252C%2522first_name%2522%253A%2522Tester%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Fa-ttgme.stel.com%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252Fu-bg7kYPKLnEznjKSycr5RbrMc9GpOPqiaBwsnNuAJSRvnDnf-et0xobMg2ZIm_v.svg%2522%257D%26chat_instance%3D-5768296595480715985%26chat_type%3Dprivate%26auth_date%3D1739628973%26signature%3DYtfMkhVohFCWnX4aJv0d3d2ZdfSi32CHL43rP0uCNU0eErqvp_7g4ToYAh4BIHQs2EPAommqYSjXRR-jw4ZeDA%26hash%3D996321b4196ac866a648a9ca521efbc886bc380bb102cd4366600b8f9aabf885",
    "bot_token": "5000851829:AAFTB2LrHs141MqjQ5VgqMVYLml4MZ4Mmwg"
}


def test_on_valid_single_encoded_init_data() -> None:
    data, bot_token = single_encoded_init_data.values()
    assert InitData(data, bot_token).validate()

def test_on_valid_double_encoded_init_data() -> None:
    data, bot_token = double_encoded_init_data.values()
    assert InitData(data, bot_token).validate(times_to_decode=2)

@pytest.mark.parametrize(
    "data, bot_token",
    [
        ("", single_encoded_init_data["bot_token"]),
        (single_encoded_init_data["data"], ""),
        ("", "")
    ]
)
def test_without_arguments(data: str, bot_token: str) -> None:
    with pytest.raises(InvalidInitDataError) as excinfo:
        InitData(data, bot_token)
        if not data and not bot_token:
            assert excinfo.value.args[0] == "Missing data and bot_token"
        elif not data:
            assert excinfo.value.args[0] == "Missing data"
        elif not bot_token:
            assert excinfo.value.args[0] == "Missing bot_token"

def test_without_hash() -> None:
    data = "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A279058397%2C%22first_name%22%3A%22Vladislav%22%2C%22last_name%22%3A%22Kibenko%22%2C%22username%22%3A%22vdkfrost%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%7D&auth_date=1662771648"
    bot_token = single_encoded_init_data["bot_token"]
    with pytest.raises(InvalidInitDataError) as excinfo:
        InitData(data, bot_token).validate()
        assert excinfo.value.args[0] == "Hash is missing"
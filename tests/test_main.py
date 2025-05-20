import pandas as pd
from main import extract_table_name, build_upload_payload


def test_extract_table_name():
    assert extract_table_name("sample.name.csv") == "sample.name"


def test_build_upload_payload_from_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("Question,Answer\nHello,World\nFoo,Bar")

    df = pd.read_csv(csv_file)
    payload = build_upload_payload(
        df,
        "my_table",
        ["Question"],
        ["Answer"],
    )

    data = payload["data"]
    assert data["name"] == "my_table"
    assert data["schema"]["searchableFields"] == ["Question"]
    assert data["schema"]["metadataFields"] == ["Answer"]
    assert data["items"] == [
        {"Question": "Hello", "Answer": "World"},
        {"Question": "Foo", "Answer": "Bar"},
    ]

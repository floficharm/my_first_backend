def test_get_books_empty(client):
    responce = client.get("/books")
    assert responce.status_code == 200
    assert responce.json() == []





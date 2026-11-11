def test_get_books_empty(client):
    responce = client.get("/books")
    assert responce.status_code == 200
    assert responce.json() == []


def test_create_book(client):
    responce = client.post("/books", json={"title": "Dude", "author": "Meme"})
    assert responce.status_code == 201
    data = responce.json()
    assert data["title"] == "Dude"
    assert data["author"] == "Meme"
    assert data["read"] is False

def test_create_book_2(client):
    responce = client.post("/books", json={"title": "Dude"})
    assert responce.status_code == 422

def test_update_book(client):
    response = client.patch("/books/999", json={"title": "Dude"})
    assert response.status_code == 404

def test_update_book_success(client):
    created = response = client.patch("/books", json={"title": "Dude", "author": "Meme"})
    book_id = created.json()["id"]

    response = client.patch(f"/books/{book_id}", json={"read": True, "rating": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["read"] is True
    assert data["rating"] == 5
    assert data["title"] == "Dude"

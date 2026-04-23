# tests/test_vote.py

def test_vote_on_post(authorized_client, test_post):
    # 1. Test a successful "Like" (dir = 1)
    res = authorized_client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 1}
    )
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_post):
    # 1. Like the post the first time
    authorized_client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 1}
    )

    # 2. Try to like it again! The server should reject this with a 409 Conflict.
    res = authorized_client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 1}
    )
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_post):
    # 1. Like the post
    authorized_client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 1}
    )

    # 2. "Unlike" the post (dir = 0)
    res = authorized_client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 0}
    )
    # The server should successfully process the unlike
    assert res.status_code == 201


def test_vote_non_exist_post(authorized_client):
    # 1. Try to like a post ID that doesn't exist in the database
    res = authorized_client.post(
        "/vote/", json={"post_id": 99999, "dir": 1}
    )
    # The server should say the post is Not Found
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_post):
    # 1. Try to vote using the naked 'client' (No JWT token)
    res = client.post(
        "/vote/", json={"post_id": test_post["id"], "dir": 1}
    )
    # The server's bouncer should block them immediately
    assert res.status_code == 401
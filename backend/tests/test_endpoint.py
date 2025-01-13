import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('endpoint, url', [
    ('users', '/api/auth/users/'),
    ('recipes', '/api/recipes/'),
    ('tags', '/api/tags/'),
    ('ingredients', '/api/ingredients/'),
])
def test_endpoint_availability(client, endpoint, url):
    print(f"Testing endpoint: {endpoint} - {url}")
    response = client.get(url)
    print(f"Response status code: {response.status_code}")
    assert response.status_code in [200, 401, 403], (
        f'Эндпоинт {endpoint} ({url}) '
        f'вернул неожиданный статус-код: {response.status_code}'
    )
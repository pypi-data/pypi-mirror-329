import pytest
import aiohttp
import responses
from utility.requesting import SyncRetryClient, AsyncRetryClient

# Fixtures
@pytest.fixture
def sync_client():
    return SyncRetryClient(retries=2, backoff_factor=0.1)

@pytest.fixture
def async_client():
    return AsyncRetryClient(retries=2, delay=0.1)

# Sync Client Tests
@responses.activate
def test_sync_get_success(sync_client):
    responses.add(
        responses.GET,
        'https://api.example.com/test',
        json={'status': 'success'},
        status=200
    )
    
    response = sync_client.get('https://api.example.com/test')
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}

@responses.activate
def test_sync_post_success(sync_client):
    responses.add(
        responses.POST,
        'https://api.example.com/test',
        json={'status': 'created'},
        status=201
    )
    
    response = sync_client.post(
        'https://api.example.com/test',
        json={'data': 'test'}
    )
    assert response.status_code == 201
    assert response.json() == {'status': 'created'}

@responses.activate
def test_sync_retry_on_failure(sync_client):
    # Add two failure responses and one success
    responses.add(
        responses.GET,
        'https://api.example.com/test',
        status=503
    )
    responses.add(
        responses.GET,
        'https://api.example.com/test',
        json={'status': 'success'},
        status=200
    )
    
    response = sync_client.get('https://api.example.com/test')
    assert response.status_code == 200
    assert len(responses.calls) > 1

# Async Client Tests
@pytest.mark.asyncio
async def test_async_get_success(async_client, aiohttp_client):
    async def mock_server(request):
        return aiohttp.web.json_response({'status': 'success'})

    app = aiohttp.web.Application()
    app.router.add_get('/test', mock_server)
    client = await aiohttp_client(app)
    
    response = await async_client.get(f'{client.make_url("/test")}')
    assert 'success' in response

@pytest.mark.asyncio
async def test_async_post_success(async_client, aiohttp_client):
    async def mock_server(request):
        return aiohttp.web.json_response({'status': 'created'}, status=201)

    app = aiohttp.web.Application()
    app.router.add_post('/test', mock_server)
    client = await aiohttp_client(app)
    
    response = await async_client.post(
        f'{client.make_url("/test")}',
        json={'data': 'test'}
    )
    assert 'created' in response

@pytest.mark.asyncio
async def test_async_retry_on_failure(async_client, aiohttp_client):
    call_count = 0
    
    async def mock_server(request):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return aiohttp.web.Response(status=503)
        return aiohttp.web.json_response({'status': 'success'})

    app = aiohttp.web.Application()
    app.router.add_get('/test', mock_server)
    client = await aiohttp_client(app)
    
    response = await async_client.get(f'{client.make_url("/test")}')
    assert 'success' in response
    assert call_count > 1

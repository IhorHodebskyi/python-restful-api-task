import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from src.database.storage import storage
from src.conf.messages import (task_not_found, task_deleted)


@pytest.fixture(autouse=True)
def clear_storage():
    storage.tasks.clear()
    storage.counter = 1


@pytest.mark.asyncio
async def test_healthchecker():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/healthchecker")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "200"
    assert "Service is running" in data["message"]


@pytest.mark.asyncio
async def test_create_task_and_get_all():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/", json={
            "title": "Test task",
            "description": "This is a test task",
            "is_completed": False
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test task"
    assert data["is_completed"] is False

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/", json={
            "title": "Test task",
            "description": "This is a test task",
            "is_completed": False
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["title"] == "Test task"
    assert data["is_completed"] is False

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Test task"


@pytest.mark.asyncio
async def test_get_task_by_id():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://tests") as ac:
        response = await ac.get("/api/tasks/1")
    assert response.status_code == 404
    assert response.json()["detail"] == task_not_found

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post("/api/tasks/", json={
            "title": "Test task",
            "description": "This is a test task",
            "is_completed": False
        })
        task_id = create_response.json()["id"]

        response = await ac.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test task"


@pytest.mark.asyncio
async def test_update_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post("/api/tasks/", json={
            "title": "Test task",
            "description": "This is a test task",
            "is_completed": False
        })
        task_id = create_response.json()["id"]

        updated_task = {
            "title": "Updated task",
            "description": "Updated description",
            "is_completed": True
        }
        response = await ac.put(f"/api/tasks/{task_id}", json=updated_task)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated task"
    assert data["is_completed"] is True

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/api/tasks/999", json=updated_task)
    assert response.status_code == 404
    assert response.json()["detail"] == task_not_found


@pytest.mark.asyncio
async def test_delete_task():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post("/api/tasks/", json={
            "title": "Task to delete",
            "description": "Will be deleted",
            "is_completed": False
        })
        task_id = create_response.json()["id"]

        response = await ac.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == task_deleted

        response = await ac.get("/api/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

        response = await ac.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == task_not_found

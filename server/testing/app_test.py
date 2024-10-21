import json
import pytest
from app import app, db, Plant

@pytest.fixture(scope='module')
def test_client():
    # Create a test client
    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()  # This is where the testing happens
        db.drop_all()  # Drop all tables after tests are done

class TestPlant:
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self, test_client):
        '''has a resource available at "/plants/<int:id>".'''
        response = test_client.get('/plants/1')
        assert response.status_code == 404  # Expecting 404 if no plant exists

    def test_plant_by_id_get_route_returns_one_plant(self, test_client):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        # First, create a plant to test with
        new_plant = Plant(name="Test Plant", image="test_image.png", price=10.0)
        db.session.add(new_plant)
        db.session.commit()

        response = test_client.get(f'/plants/{new_plant.id}')
        data = json.loads(response.data.decode())

        assert type(data) == dict
        assert data["id"] == new_plant.id
        assert data["name"] == new_plant.name

    def test_plant_by_id_patch_route_updates_is_in_stock(self, test_client):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        new_plant = Plant(name="Patch Plant", image="patch_image.png", price=15.0, is_in_stock=True)
        db.session.add(new_plant)
        db.session.commit()
        
        response = test_client.patch(
            f'/plants/{new_plant.id}',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert type(data) == dict
        assert data["id"] == new_plant.id
        assert data["is_in_stock"] is False

    def test_plant_by_id_delete_route_deletes_plant(self, test_client):
        '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
        new_plant = Plant(
            name="Live Oak",
            image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            price=250.00,
            is_in_stock=False,
        )
        
        db.session.add(new_plant)
        db.session.commit()
        
        response = test_client.delete(f'/plants/{new_plant.id}')
        assert response.status_code == 204  # Expecting 204 No Content

        # Check if plant is deleted
        response = test_client.get(f'/plants/{new_plant.id}')
        assert response.status_code == 404  # Expecting 404 if the plant was deleted

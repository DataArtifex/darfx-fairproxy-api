from fairproxy_api.dependencies import get_server_repository
from fairproxy_api.main import app
from fairproxy_api.repositories.yaml_server import YamlServerRepository
from fastapi.testclient import TestClient

client = TestClient(app)


def test_status_endpoint():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "pass", "version": "0.1.0"}


def test_socrata_dcat():
    response = client.get("/socrata/data.cityofnewyork.us/uvpi-gqnh/dcat")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/ld+json"


def test_socrata_unified_dcat():
    response = client.get("/datasets/urn:socrata:data.cityofnewyork.us:uvpi-gqnh/dcat")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/ld+json"


def test_unsupported_unified_platform():
    response = client.get("/datasets/urn:mtnards:rds.highvalueata.net:catalog:dataset/dcat")
    assert response.status_code == 501
    assert "experimental" in response.json()["detail"]


def test_resources_placeholder():
    response = client.get("/resources/")
    assert response.status_code == 200


def test_vocab_placeholder():
    response = client.get("/vocab/")
    assert response.status_code == 200


# Servers Route Tests
def override_get_server_repository():
    return YamlServerRepository()


app.dependency_overrides[get_server_repository] = override_get_server_repository


def test_servers_get_all():
    response = client.get("/servers/")
    assert response.status_code == 200
    servers = response.json()
    assert isinstance(servers, list)
    assert len(servers) > 0  # servers.yaml has multiple entries


def test_servers_get_by_id():
    response = client.get("/servers/data.cityofchicago.org")
    assert response.status_code == 200
    server = response.json()
    assert server["id"] == "data.cityofchicago.org"
    assert server["platform"] == "socrata"


def test_servers_get_by_id_missing():
    response = client.get("/servers/does_not_exist_at_all")
    assert response.status_code == 404


# Catalog Route Tests
def test_catalog_resolve():
    response = client.get("/catalog/urn:socrata:data.cityofnewyork.us")
    assert response.status_code == 200
    res = response.json()
    assert res["type"] == "Catalog"
    assert res["host"] == "data.cityofnewyork.us"


def test_catalog_dcat():
    response = client.get("/catalog/urn:socrata:data.cityofnewyork.us/dcat")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/ld+json"

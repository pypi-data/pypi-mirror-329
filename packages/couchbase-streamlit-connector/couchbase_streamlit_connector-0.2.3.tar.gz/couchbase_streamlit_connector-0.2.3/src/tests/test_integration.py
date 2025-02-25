from couchbase_streamlit_connector.connector import CouchbaseConnector
import streamlit as st

import os

from couchbase.exceptions import DocumentNotFoundException
from couchbase.logic.n1ql import QueryStatus
from dotenv import load_dotenv

import pytest
     
@pytest.fixture
def connection():
    assert load_dotenv()
    assert os.getenv("CONNSTR"), "CONNSTR is not set"
    assert os.getenv("USERNAME"), "USERNAME is not set"
    assert os.getenv("PASSWORD"), "PASSWORD is not set"
    assert os.getenv("BUCKET_NAME"), "BUCKET_NAME is not set"
    assert os.getenv("SCOPE_NAME"), "SCOPE_NAME is not set"
    assert os.getenv("COLLECTION_NAME"), "COLLECTION_NAME is not set"
    
    connection = st.connection(
        "couchbase", 
        type=CouchbaseConnector, 
        CONNSTR= os.getenv("CONNSTR"),
        USERNAME= os.getenv("USERNAME"),
        PASSWORD= os.getenv("PASSWORD"),
        BUCKET_NAME= os.getenv("BUCKET_NAME"),
        SCOPE_NAME= os.getenv("SCOPE_NAME"),
        COLLECTION_NAME= os.getenv("COLLECTION_NAME")
    )
    return connection
    
def test_create(connection):
    """Test the successful creation of an airline"""
    airline_data = {
        "name": "Sample Airline",
        "iata": "SAL",
        "icao": "SALL",
        "callsign": "SAM",
        "country": "Sample Country",
    }
    document_id = "airline_test_insert"
    try:
        connection.collection.remove(document_id)
    except DocumentNotFoundException:
        pass
    response = connection.insert_document(document_id, airline_data)
    assert response.key == document_id

    # Check document stored in DB is same as sent & clean up
    doc_in_db = connection.get_document(document_id)
    assert doc_in_db == airline_data
    connection.remove_document(document_id)
            
def test_read(connection):
    """Test the reading of an airline"""
    airline_data = {
        "name": "Sample Airline",
        "iata": "SAL",
        "icao": "SALL",
        "callsign": "SAM",
        "country": "Sample Country",
    }
    document_id = "airline_test_read"
    try:
        connection.collection.remove(document_id)
    except DocumentNotFoundException:
        pass
    response = connection.insert_document(document_id, airline_data)

    response = connection.get_document(document_id)
    assert response == airline_data
    connection.remove_document(document_id)
    
def test_update(connection):
    """Test updating an existing airline"""
    airline_data = {
        "name": "Sample Airline",
        "iata": "SAL",
        "icao": "SALL",
        "callsign": "SAM",
        "country": "Sample Country",
    }
    document_id = "airline_test_update"
    try:
        connection.collection.remove(document_id)
    except DocumentNotFoundException:
        pass
    response = connection.insert_document(document_id, airline_data)

    updated_airline_data = {
        "name": "Updated Airline",
        "iata": "SAL",
        "icao": "SALL",
        "callsign": "SAM",
        "country": "Updated Country",
    }

    response = connection.replace_document(document_id, updated_airline_data)
    assert response.key == document_id
    response = connection.get_document(document_id)
    assert response == updated_airline_data

    connection.remove_document(document_id)
    
def test_delete(connection):
    """Test deleting an existing airline"""
    airline_data = {
        "name": "Sample Airline",
        "iata": "SAL",
        "icao": "SALL",
        "callsign": "SAM",
        "country": "Sample Country",
    }
    document_id = "airline_test_delete"
    try:
        connection.collection.remove(document_id)
    except DocumentNotFoundException:
        pass
    response = connection.insert_document(document_id, airline_data)

    response = connection.remove_document(document_id)
    assert response.key == document_id
    
def test_query(connection):
    """Test the destination airports from an airline"""
    query = """
        SELECT * FROM `travel-sample`.`inventory`.`airline`
        WHERE type = "airline"
        AND country = "United States"
        LIMIT 5;
    """
    result = connection.query(query)
    data = []
    for row in result.rows():
        data.append(row)
    assert result.metadata().status() == QueryStatus.SUCCESS

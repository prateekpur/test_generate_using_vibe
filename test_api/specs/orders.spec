endpoint_spec = {
    "path": "/orders",
    "method": "POST",
    "has_auth_header": True,
    "request_body_schema": {
        "item_id": {"type": "string", "minLength": 1},
        "quantity": {"type": "integer", "minimum": 1, "maximum": 10}
    },
    "responses": [201, 400, 401, 422]
}

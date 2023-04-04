def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_upsert_assignment_student_1(client, h_student_1):
    content = 'Edited content of Assignment'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 2,
            'content': content
        }
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["content"] == content

def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_upsert_only_draft_assignment(client, h_student_1):
    content = 'Edited content of Assignment'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 2,
            'content': content
        }
    )

    response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert data['message'] == 'only assignment in draft state can be edited'

def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Only draft assignment can be submitted'

def test_submit_draft_assignment_student_2(client, h_student_2):
    # First, create a new draft assignment for student_2
    content = 'EFGH TESTPOST'
    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'content': content
        })
    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

    # Then, try to submit the draft assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': data['id'],
            'teacher_id': 2
        })
    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 2
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2
import webdb.interface as interface
import webdb.cache as cache

def filter_response_ids_by_content_type(cursor, response_ids, content_type):

    content_type_id = cache.get_content_type_id(cursor, content_type)

    response_ids_str = ",".join(str(x) for x in response_ids)

    sql = ("SELECT ID FROM RESPONSES WHERE "
           "CONTENT_TYPE_ID = :content_type_id AND "
           "ID IN("+response_ids_str+")"
           "")

    params = {
        'content_type_id' : content_type_id
    }
    
    cursor.execute(sql, params)

    return [x[0] for x in cursor.fetchall() ]

def get_requests_of_session_id_and_content_type(cursor, session_id, content_type):
    
    request_list = interface.get_request_list_of_session_id(cursor, session_id)

    filtered_response_id_list = filter_response_ids_by_content_type(
        cursor, 
        (x[1]['response_id'] for x in request_list), 
        content_type
    )

    filtered_response_id_set = set(filtered_response_id_list)

    return [x for x in request_list if x[1]['response_id'] in filtered_response_id_set]





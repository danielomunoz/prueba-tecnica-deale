import json
import uuid



def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response


def isThereBodyInRequest(supposedBody):
    try:
        requestBody = json.loads(supposedBody)

        return True, requestBody, None
    except:
        errorBody = {
            'ok': False,
            'message': 'You need to attach a valid json body to the request'
        }

        return False, None, errorBody


def validateOrgIdInBody(requestBody):
    if 'org_id' not in requestBody:
        errorBody = {
            'ok': False,
            'message': 'Error! Organization ID (org_id field in body) is needed'
        }

        return False, errorBody
    
    try:
        str(uuid.UUID(requestBody['org_id']))

        return True, None
    except:
        errorBody = {
            'ok': False,
            'message': 'Error! Organization ID (org_id field in body) must be a valid UUID in String format'
        }

        return False, errorBody


def validateFavouriteOrgIdInBody(requestBody):
    if 'favourite_org_id' not in requestBody:
        errorBody = {
            'ok': False,
            'message': 'Error! Favourite Organization ID (favourite_org_id field in body) is needed'
        }

        return False, errorBody
    
    try:
        str(uuid.UUID(requestBody['favourite_org_id']))

        return True, None
    except:
        errorBody = {
            'ok': False,
            'message': 'Error! Organization ID (org_id field in body) must be a valid UUID in String format'
        }

        return False, errorBody


def checkItemsInDbWithSameParams(supposedItemsInDatabaseWithSameParams):
    if len(supposedItemsInDatabaseWithSameParams) != 0:
        errorBody = {
            'ok': False,
            'message': 'Error! This favourite organization relationship is already in database'
        }

        return True, errorBody
    
    return False, None

import json
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime
import uuid


dynamodbTableName = 'favouriteOrganizationTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)


def getAllFavouritesOrganizations(event, context):
    try:
        db_response = table.scan()
        result = db_response['Items']
        
        body = {
            'ok': True,
            'message': 'Favourite Organizations found!',
            'favouriteOrganizations': result
        }

        return buildResponse(200, body)
    
    except:
        body = {
            'ok': False,
            'message': 'Some error ocurred when retrieveng Favourite Organizations from database'
        }

        return buildResponse(500, body)


def postFavouriteOrganization(event, context):
    try:
        request_body = json.loads(event['body'])

        if 'org_id' not in request_body:
            body = {
                'ok': False,
                'message': 'Error! Organization ID (org_id field in body) is needed'
            }

            return buildResponse(400, body)
        
        if 'favourite_org_id' not in request_body:
            body = {
                'ok': False,
                'message': 'Error! Favourite Organization ID (favourite_org_id field in body) is needed'
            }

            return buildResponse(400, body)
        
        db_response = table.scan(FilterExpression=Attr('org_id').eq(request_body['org_id'])
                                    & Attr('favourite_org_id').eq(request_body['favourite_org_id']))
        if len(db_response['Items']) != 0:
            body = {
                'ok': False,
                'message': 'Error! This favourite organization relationship is already in database'
            }

            return buildResponse(403, body)

        request_body['id'] = str(uuid.uuid4())
        
        now = datetime.now()
        request_body['date'] = now.isoformat()

        table.put_item(Item=request_body)

        body = {
            'ok': True,
            'message': 'Success! New Favourite Organization created in database',
            'favouriteOrganization': request_body
        }

        return buildResponse(200, body)
    
    except:
        body = {
            'ok': False,
            'message': 'Some error ocurred when creating a new Favourite Organization in database. Remember that you need to attach a json body to the request with the following fields: [org_id, favourite_org_id]'
        }

        return buildResponse(500, body)


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

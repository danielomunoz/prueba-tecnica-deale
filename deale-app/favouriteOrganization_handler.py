from datetime import datetime
import uuid

import boto3
from boto3.dynamodb.conditions import Attr

from utils import *


dynamodbTableName = 'favouriteOrganizationTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)


def getAllFavouritesOrganizations(event, context):
    try:
        db_response = table.scan()
        result = db_response['Items']
        
        response_body = {
            'ok': True,
            'message': 'Favourite Organizations found!',
            'resultKey': 'favouriteOrganizations',
            'favouriteOrganizations': result
        }

        return buildResponse(200, response_body)
    except:
        response_body = {
            'ok': False,
            'message': 'Internal server error when retrieveng Favourite Organizations from database'
        }

        return buildResponse(500, response_body)


def postFavouriteOrganization(event, context):
    try:
        there_is_body_in_request, request_body, error_body = isThereBodyInRequest(event['body'])
        if not there_is_body_in_request:
            return buildResponse(400, error_body)
        
        there_is_a_valid_org_id_in_request, error_body = validateOrgIdInBody(request_body)
        if not there_is_a_valid_org_id_in_request:
            return buildResponse(400, error_body)
        
        there_is_a_valid_favourite_org_id_in_request, error_body = validateFavouriteOrgIdInBody(request_body)
        if not there_is_a_valid_favourite_org_id_in_request:
            return buildResponse(400, error_body)
        
        db_response = table.scan(FilterExpression=Attr('org_id').eq(request_body['org_id'])
                                    & Attr('favourite_org_id').eq(request_body['favourite_org_id']))
        
        items_in_db_with_same_params = db_response['Items']
        
        there_are_items_in_db_with_same_params, errorBody = checkItemsInDbWithSameParams(items_in_db_with_same_params)
        if there_are_items_in_db_with_same_params:
            return buildResponse(400, errorBody)

        request_body['id'] = str(uuid.uuid4())
        
        now = datetime.now()
        request_body['date'] = now.isoformat()

        table.put_item(Item=request_body)

        response_body = {
            'ok': True,
            'message': 'Success! New Favourite Organization created in database',
            'resultKey': 'favouriteOrganization',
            'favouriteOrganization': request_body
        }

        return buildResponse(200, response_body)
    
    except:
        response_body = {
            'ok': False,
            'message': 'Internal server error when creating a new Favourite Organization in database'
        }

        return buildResponse(500, response_body)

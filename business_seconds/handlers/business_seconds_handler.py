from pyramid.view import view_config
from datetime import datetime
from pyramid.response import Response as PyramidResponse


@view_config(
    route_name='get_business_seconds', request_method='GET', openapi=True
)
def get_business_seconds(request):
    path_params = request.openapi_validated.parameters.query
    print(f"Path parameters: {path_params}")
    try:
        start_time: str = path_params['start_time']
        start = datetime.fromisoformat(start_time)
        end_time: str = path_params['end_time']
        end =  datetime.fromisoformat(end_time)
    except ValueError:
        return PyramidResponse(
            json={
                'error': 'Start time and End time should be in isoformat'
            },
            status=400,
        )
    except KeyError:
        return PyramidResponse(
            json={
                "error": "Invalid key found in path params"
            },
            status=400
        )
    response = request.registry.business_controller.business_seconds(start, end)
    print(f"Response from controller = {response} and type: {type(response)}")
    return PyramidResponse(
        json={
            "business_seconds": int(response) if response else int('0')
        },
        status=200
    )

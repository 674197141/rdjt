import json
from functools import wraps
from inspect import signature
from typing import Optional, Callable, TypeVar, Any, Union, Iterable, Type, List

from flask import request, jsonify, make_response, Response, abort
from pydantic import BaseModel, ValidationError

from .exceptions import InvalidIterableOfModelsException, ManyModelValidationError

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass

InputParams = TypeVar("InputParams")


def make_json_response(
        content: Union[BaseModel, Iterable[BaseModel]],
        status_code: int,
        exclude_none: bool = False,
        many: bool = False,
) -> Response:
    """serializes model, creates JSON response with given status code"""
    if many:
        js = f"[{', '.join([model.json(exclude_none=exclude_none) for model in content])}]"
    else:
        js = content.json(exclude_none=exclude_none)
    response = make_response(js, status_code)
    response.mimetype = "application/json"
    return response


def is_iterable_of_models(content: Any) -> bool:
    try:
        return all(isinstance(obj, BaseModel) for obj in content)
    except TypeError:
        return False


def validate_many_models(model: Type[BaseModel], content: Any) -> List[BaseModel]:
    try:
        return [model(**fields) for fields in content]
    except TypeError:
        # iteration through `content` fails
        err = [
            {
                "loc": ["root"],
                "msg": "is not an array of objects",
                "type": "type_error.array",
            }
        ]
        raise ManyModelValidationError(err)
    except ValidationError as ve:
        raise ManyModelValidationError(ve.errors())


def validate(
        body: Optional[Type[BaseModel]] = None,
        query: Optional[Type[BaseModel]] = None,
        on_success_status: int = 200,
        exclude_none: bool = False,
        response_many: bool = False,
        request_body_many: bool = False,
):
    """
    Decorator for route methods which will validate query and body parameters
    as well as serialize the response (if it derives from pydantic's BaseModel
    class).

    Request parameters are accessible via flask's `request` variable:
        - request.query_params
        - request.body_params

    `exclude_none` whether to remove None fields from response
    `response_many` whether content of response consists of many objects
        (e. g. List[BaseModel]). Resulting response will be an array of serialized
        models.
    `request_body_many` whether response body contains array of given model
        (request.body_params then contains list of models i. e. List[BaseModel])

    example:

    from flask import request
    from flask_pydantic import validate
    from pydantic import BaseModel

    class Query(BaseModel):
        query: str

    class Body(BaseModel):
        color: str

    class MyModel(BaseModel):
        id: int
        color: str
        description: str

    ...

    @app.route("/")
    @validate(query=Query, body=Body)
    def test_route():
        query = request.query_params.query
        color = request.body_params.query

        return MyModel(...)

    -> that will render JSON response with serialized MyModel instance
    """

    def decorate(func: Callable[[InputParams], Any]) -> Callable[[InputParams], Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            q, b, err = None, None, {}
            # body_params = request.get_json()
            # query_params = request.args
            if query:
                # query_params = request.args
                data = request.data
                if data and data != "''":
                    query_params = json.loads(data)
                else:
                    query_params = request.args
                try:
                    q = query(**query_params)
                except ValidationError as ve:
                    err["query_params"] = ve.errors()
            if body:
                body_params = json.loads(request.data)
                # body_params = request.get_json()
                if request_body_many:
                    try:
                        b = validate_many_models(body, body_params)
                    except ManyModelValidationError as e:
                        err["body_params"] = e.errors()
                else:
                    try:
                        b = body(**body_params)
                    except ValidationError as ve:
                        err["body_params"] = ve.errors()
            # request.query_params = q
            # request.body_params = b
            request.params = q if q else b
            if err:
                abort(make_response(jsonify({"validation_error": err}), 400))
            res = func(*args, **kwargs)

            if response_many:
                if is_iterable_of_models(res):
                    return make_json_response(
                        res, on_success_status, exclude_none, True
                    )
                else:
                    raise InvalidIterableOfModelsException(res)

            if isinstance(res, BaseModel):
                return make_json_response(
                    res, on_success_status, exclude_none=exclude_none
                )

            if (
                    isinstance(res, tuple)
                    and len(res) == 2
                    and isinstance(res[0], BaseModel)
            ):
                return make_json_response(res[0], res[1], exclude_none=exclude_none)

            return res

        return wrapper

    return decorate


def decorate(func: Callable[[InputParams], Any]) -> Callable[[InputParams], Any]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_data = signature(func)
        query_model = func_data.parameters.get('query_model')
        body_model = func_data.parameters.get('body_model')
        q, b, err = None, None, {}
        if query_model:
            query_params = request.args
            model = query_model.annotation
            try:
                q = model(**query_params)
                kwargs['query_model'] = q
            except ValidationError as ve:
                err["query_params"] = ve.errors()
        if body_model:
            body_params = request.get_json() if request.get_json() else request.values
            model = body_model.annotation
            try:
                b = model(**body_params)
                kwargs['body_model'] = b
            except ValidationError as ve:
                err["body_params"] = ve.errors()

        if err:
            return make_response(jsonify({"validation_error": err}), 400)
        res = func(*args, **kwargs)

        return res

    return wrapper

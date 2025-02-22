"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from typing import TypeVar, List, Generic, Type, Optional

from pydantic import BaseModel

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from nomenclators_archetype.domain.commons import NomenclatorId
from nomenclators_archetype.domain.exceptions import RequiredElementError
from nomenclators_archetype.domain.repository.builders import Pageable
from nomenclators_archetype.domain.repository.commons import RepositoryOperationError, RepositoryIntegrityError
from nomenclators_archetype.domain.service.commons import NomenclatorService
from nomenclators_archetype.domain.usecase.commons import BaseUseCase

from nomenclators_archetype.infrastructure.http.mappers import SchemaBaseNomenclatorMapper
from nomenclators_archetype.infrastructure.http.schemas import SchemaQueryParam
from nomenclators_archetype.infrastructure.http.schemas import SchemaSimpleNomenclatorCreator, SchemaSimpleNomenclatorUpdater

from nomenclators_archetype.infrastructure.http.exceptions import ForbiddenException, NotFoundException, ConflictException
from nomenclators_archetype.infrastructure.http.exceptions import UnprocessableEntityException

# Mapper class representation
M = TypeVar('M', bound=SchemaBaseNomenclatorMapper)
R = TypeVar('R', bound=BaseModel)  # Response class representation
# Creator class representation
C = TypeVar('C', bound=SchemaSimpleNomenclatorCreator)
# Updater class representation
U = TypeVar('U', bound=SchemaSimpleNomenclatorUpdater)


class BaseNomenclatorRouter(APIRouter, Generic[M, R, C, U]):
    """Base Nomenclator Router class"""

    def __init__(self, *args,
                 service: NomenclatorService, mapper: Type[M],
                 creator_uc: BaseUseCase, updater_uc: BaseUseCase, deleter_uc: BaseUseCase,
                 default_name: str = "Default", **kwargs):
        """Constructor for BaseNomenclatorRouter class"""

        if service is None:
            raise RequiredElementError(
                "Service is required: The service for router is not defined")
        if mapper is None:
            raise RequiredElementError(
                "Mapper is required: The Mapper for router is not defined")

        super().__init__(*args, **kwargs)

        self.name = default_name
        self.service = service
        self.mapper = mapper

        self.creator_use_case = creator_uc
        self.updater_use_case = updater_uc
        self.deleter_use_case = deleter_uc

        self._include_default_routes()

    def _include_default_routes(self):
        """Include or register default nomenclator routes."""

        @self.post("/status", status_code=status.HTTP_200_OK, tags=[self.name], name=f"Status for API: {self.name} nomenclator")
        async def get_status():
            return JSONResponse(content={"message": "API is running"}, status_code=200)

        @self.post(
            "/", response_model=List[R],
            status_code=status.HTTP_200_OK, tags=[self.name],
            name=f"List of {self.name}'s",
        )
        async def list_items(param: Optional[SchemaQueryParam] = Body(default=None)) -> List[R]:
            try:

                return [
                    self.mapper.map_from_domain_to_schema(domain)
                    for domain in self.service.list_items(
                        pageable=Pageable(
                            page=param.pagination.page,
                            size=param.pagination.element_for_page,
                            pagination=True,
                            sort=param.pagination.sort_mapped()

                        ) if param and param.pagination else None,
                        filters=param.filter.mapped(
                            self.mapper.map_attributes()) if param and param.filter else None,
                    )
                ]
            except (ValueError, RequiredElementError, NotImplementedError, RepositoryOperationError) as e:
                raise ForbiddenException(
                    message=f"Error listing items from {self.name} repository ({e}).") from e

        @self.get(
            "/{_id}", response_model=R,
            status_code=status.HTTP_200_OK, tags=[self.name],
            name=f"Get {self.name} item by Id",
        )
        async def get_item_by_id(_id: NomenclatorId) -> R:
            try:
                domain = self.service.get_item_by_id(_id)
                if not domain:
                    raise NotFoundException(
                        message=f"Item Id: {_id} for {self.name} repository not found")

                return self.mapper.map_from_domain_to_schema(domain)
            except (ValueError, RequiredElementError, NotImplementedError, RepositoryOperationError) as e:
                raise NotFoundException(
                    message=f"Error getting item Id: {_id} from {self.name} repository ({e}).") from e

        @self.delete(
            "/{_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=[self.name],
            name=f"Delete {self.name} item by Id",
        )
        async def delete_item_by_id(_id: NomenclatorId):
            try:
                self.deleter_use_case.invoke(_id)
            except (RequiredElementError, NotImplementedError, RepositoryOperationError) as e:
                raise NotFoundException(
                    message=f"Error deleting item Id: {_id} from {self.name} repository ({e}).") from e

        @self.put(
            "/", response_model=R,
            status_code=status.HTTP_202_ACCEPTED, tags=[self.name],
            name=f"Update {self.name} item by Id",
        )
        async def update_item_by_id(item: U = Body(...)) -> R:
            try:
                return self.mapper.map_from_domain_to_schema(
                    self.updater_use_case.invoke(
                        self.mapper.map_from_schema_to_domain(item)
                    )
                )
            except (ValueError, RequiredElementError, NotImplementedError, RepositoryIntegrityError, RepositoryOperationError) as e:
                raise NotFoundException(
                    message=f"Error updating item : {item} from {self.name} repository ({e}).") from e

        @self.post(
            "/create", response_model=R,
            status_code=status.HTTP_201_CREATED, tags=[self.name],
            name=f"Create {self.name} item",
        )
        async def create_item(item: C = Body(...)) -> R:
            try:
                return self.mapper.map_from_domain_to_schema(
                    self.creator_use_case.invoke(
                        self.mapper.map_from_schema_to_domain(item)
                    )
                )
            except (RepositoryIntegrityError, RepositoryOperationError) as e:
                raise ConflictException(
                    f"Error creating item on {self.name} repository ({e}).") from e
            except Exception as e:
                raise UnprocessableEntityException(
                    f"Error creating item on {self.name} repository ({e}).") from e

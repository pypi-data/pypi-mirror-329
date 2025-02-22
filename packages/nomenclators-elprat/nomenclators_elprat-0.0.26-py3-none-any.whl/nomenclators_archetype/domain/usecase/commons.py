"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, TypeVarTuple, Optional, Union

from nomenclators_archetype.domain.exceptions import RequiredElementError

R = TypeVar('R', bound=object)  # Response class representation

P = TypeVarTuple('P')  # Property class representation


class BaseUseCase(ABC, Generic[R, *P]):
    """Base class for use cases"""

    def __init__(self, services: Optional[Union[object, dict[str, object]]] = None):
        if isinstance(services, dict):
            self.__dict__[
                "_services"] = services if services is not None else {}
        elif services is not None:
            self.__dict__["_services"] = {"service": services}

    def __getattr__(self, property_name) -> P:  # type: ignore

        if property_name in self.__dict__:
            return self.__dict__[property_name]

        services = self.__dict__.get("_services", {})
        if property_name in services:
            return services[property_name]  # type: ignore
        raise RequiredElementError(
            f"The services '{property_name}' or the property '{property_name}', isn't defined on UseCase")

    def __dir__(self):
        base_attrs = list(super().__dir__())
        instance_attrs = list(self.__dict__.keys())
        services_attrs = list(self.__dict__.get("_services", {}).keys())
        return sorted(set(base_attrs + instance_attrs + services_attrs))

    @abstractmethod
    def invoke(self, *params) -> R:
        """Invoke the use case"""
        raise NotImplementedError


class UseCaseIsolatedSession(BaseUseCase, Generic[R, *P]):
    """Use Case isolated session class"""

    def __init__(self, session_factory, services: Optional[Union[object, dict[str, object]]] = None):
        super().__init__(services)
        self._session_factory = session_factory


class UseCaseSharedSession(BaseUseCase, Generic[R, *P]):
    """Use Case shared session class"""

    def __init__(self, db_session, services: Optional[Union[object, dict[str, object]]] = None):
        super().__init__(services)
        self.session = db_session

        if isinstance(services, dict):
            for service in services.values():
                service.set_session(db_session)  # type: ignore
        else:
            services.set_session(db_session)  # type: ignore

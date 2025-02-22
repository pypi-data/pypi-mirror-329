"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import abstractmethod
from typing import Type, Optional, TypeVar, Protocol, List

from nomenclators_archetype.domain.exceptions import RequiredElementError
from nomenclators_archetype.domain.repository.builders import Pageable

I = TypeVar('I', bound=object)  # Intentifier class representation
E = TypeVar('E', bound=object)  # Persistence Entity class representation
S = TypeVar('S', bound=object)  # Session class representation
B = TypeVar('B', bound=object)  # Query Builder class representation


class RepositoryOperationError(Exception):
    """RepositoryOperationError exception Class"""


class RepositoryIntegrityError(Exception):
    """RepositoryIntegrityError exception Class"""


class CrudRepository(Protocol[I, E, S, B]):  # type: ignore
    """CrudRepository Class"""

    _session: Optional[S]
    _builder: Optional[B]
    _entity: Optional[Type[E]]

    def __init__(self, session: Optional[S], builder: Optional[B], entity: Optional[Type[E]] = None):
        pass

    @property
    def session(self) -> S:
        """Get session"""
        if self._session:
            return self._session
        else:
            raise NotImplementedError(
                "The session must be injected on the class by constructor or setter")

    def set_session(self, new_session):
        """Set session"""
        self._session = new_session

    @property
    def builder(self) -> B:
        """Get builder"""
        if not hasattr(self, "_builder") or self._builder is None:
            self._builder = self.get_query_builder()
        return self._builder

    @property
    def entity(self) -> Type[E]:
        """Get entity"""
        if not hasattr(self, "_entity") or self._entity is None:
            self._entity = self.get_entity_model_class()
        else:
            child_model = self.get_entity_model_class()
            if issubclass(child_model, self._entity) and child_model is not self._entity:
                self._entity = child_model

        return self._entity

    def get_entity_model_class(self) -> Type[E]:
        """Get persistence type class"""
        raise NotImplementedError(
            "The entity model definition must be injected by constructor or implemented by subclasses")

    def get_query_builder(self) -> B:
        """Get query builder operator for repository class"""
        raise NotImplementedError(
            "The query_builder class must be injected by constructor or implemented by subclasses")

    def save(self, entity: E) -> E:
        """Save an entity (create or update)."""
        try:
            self.session.add(entity)  # type: ignore
            return entity
        except Exception as e:  # pylint: disable=broad-except
            if type(e).__name__ == "IntegrityError":
                raise RepositoryIntegrityError(
                    "Error on create entity: Integrity Error ({e}).") from e
            else:
                raise RepositoryOperationError(
                    "Error on create entity ({e}).") from e

    def update(self, updated_entity: E) -> E:
        """Update an entity."""
        try:
            entity = self.get_by_id_lazy_select(
                updated_entity.id)  # type: ignore

            if not entity:
                raise RequiredElementError(
                    f"Entity with id {updated_entity.id} not found")  # type: ignore
            if not entity.active:  # type: ignore
                raise RepositoryOperationError(
                    f"The entity ID {updated_entity.id} cannot be updated")  # type: ignore

            return self.session.merge(updated_entity)  # type: ignore
        except Exception as e:  # pylint: disable=broad-except
            if type(e).__name__ == "IntegrityError" or type(e).__name__ == "StatementError":
                raise RepositoryIntegrityError(
                    "Error on create entity: Integrity Error ({e}).") from e
            else:
                raise RepositoryOperationError(
                    "Error on update entity ({e}).") from e

    def update_by_id(self, _id: I, updated_entity: E):
        """Update an entity by its id."""

        entity = self.get_by_id(_id)
        if not entity:
            raise RequiredElementError(f"Entity with id {_id} not found")
        elif entity.active is False:  # type: ignore
            raise RepositoryOperationError(
                f"The entity ID {entity.id} cannot be updated")  # type: ignore

        changes = self.mapper_entity_to_dict(updated_entity)

        for field, value in changes.items():
            if hasattr(entity, field) and value is not None:
                setattr(entity, field, value)

    def delete(self, entity: E):
        """Remove of an entity."""
        self.session.delete(entity)  # type: ignore

    def delete_by_id(self, _id: I):
        """Removes an entity by its id."""
        entity = self.get_by_id(_id)
        if entity:
            self.delete(entity)
        else:
            raise RequiredElementError(f"Entity with id {_id} not found")

    def delete_all(self):
        """Removes all entities."""
        query = self.create_builder().build()
        query.delete()

    def create_builder(self):
        """Create a new query builder instance"""
        return self.builder.set_session(self.session).set_model(self.entity)  # type: ignore

    def get_by_id(self, _id: I) -> E:
        """Get domain element by ID"""
        query = self.create_builder().build()
        return query.filter_by(id=_id).first()

    def get_by_id_lazy_select(self,  _id: I) -> E:
        """Get domain element by ID in mode lazy / select."""
        return self.session.get(self.entity, _id)  # type: ignore

    @abstractmethod
    def mapper_entity_to_dict(self, entity: E) -> dict:
        """Transform an entity to a dictionary."""

    def get_all(self) -> List[E]:
        """Retrieves all entities."""
        query = self.create_builder().build()
        return query.filter_by(active=True).all()

    def get_garbage_all(self) -> List[E]:
        """Retrieves all entities deleted that exist on garbage collector."""
        query = self.create_builder().build()
        return query.filter_by(active=False).all()

    def garbage_recover(self, entity: E):
        """Recover an entity from garbage collector."""
        if not entity.active:  # type: ignore
            entity.active = True  # type: ignore
            self.update(entity)
        else:
            raise RequiredElementError(
                f"The entity ID {entity.id} is not deleted")  # type: ignore

    def garbage_recover_by_id(self, _id: I):
        """Recover an entity from garbage collector by its id."""
        entity = self.get_by_id(_id)
        if entity:
            self.garbage_recover(entity)


class PagingAndSortingRepository(CrudRepository[I, E, S, B]):
    """PagingAndSortingRepository Class"""

    @abstractmethod
    def mapper_entity_to_dict(self, entity: E) -> dict:
        """Transform an entity to a dictionary."""

    def get_all(self, pageable: Optional[Pageable] = None) -> List[E]:
        """Retrieves pageable and sorted entities."""
        query = self.create_builder().set_options(pageable).build()
        return query.filter_by(active=True).all()


class JpaRepository(PagingAndSortingRepository[I, E, S, B]):
    """JpaRepository Class"""

    @abstractmethod
    def mapper_entity_to_dict(self, entity: E) -> dict:
        """Transform an entity to a dictionary."""

    def get_all(self, pageable: Optional[Pageable] = None, filters: Optional[dict] = None,
                group_by: Optional[list] = None, group_by_id: Optional[str] = None) -> List[E]:
        """
        Get all items: if defined retrieves each item list, pageable, sorted and groupped.

        :param pageable: Pageable object
        :param filters: Filters object
        :param group_by: Group by object
        :param group_by_id: Group by id object
        """
        query = self.create_builder().set_filter({'active': True}).set_filter(filters).set_group(
            group_by, group_by_id).set_options(pageable).build()

        return query.all()

    def save_and_flush(self, entity: E) -> E:
        """Save an entity and sync immediately."""
        self.save(entity)
        self.session.flush()  # type: ignore
        return entity

    def create(self, entity: E) -> E:
        """Create a new entity."""
        return self.save_and_flush(entity)

    def delete_all_in_batch(self):
        """Removes all entities in a single operation."""
        query = self.create_builder().build()
        query.delete(synchronize_session=False)

    def delete_all_by_id_in_batch(self, ids):
        """Removes multiple entities by their ids in a single operation."""
        query = self.create_builder().build()
        query.filter(self.entity.id.in_(ids)).delete(  # type: ignore
            synchronize_session=False)

    def find_by_spec(self, spec, pageable: Optional[Pageable] = None) -> List[E]:
        """Allows dynamic queries based on criteria."""
        query = self.create_builder().set_options(pageable).build()
        return query.filter(spec).all()

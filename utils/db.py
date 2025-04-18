"""
Database utility functions for the savings app.
"""
from app import db
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def db_transaction():
    """
    Context manager for database transactions.
    Automatically handles commit and rollback on exceptions.
    
    Usage:
        with db_transaction():
            # database operations here
    """
    try:
        yield
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction error: {str(e)}")
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error during database transaction: {str(e)}")
        raise

def paginate_query(query, page=1, per_page=20):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        dict: Pagination info with items and metadata
    """
    if page < 1:
        page = 1
    
    if per_page > 100:
        per_page = 100
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        "items": paginated.items,
        "pagination": {
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
            "next_page": paginated.next_num,
            "prev_page": paginated.prev_num
        }
    }

def execute_bulk_insert(model, items):
    """
    Efficiently insert multiple items into the database.
    
    Args:
        model: SQLAlchemy model class
        items: List of dictionaries containing model attribute values
        
    Returns:
        bool: Success status
    """
    try:
        db.session.bulk_insert_mappings(model, items)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Bulk insert error: {str(e)}")
        return False

def get_or_create(model, **kwargs):
    """
    Get an existing instance or create a new one.
    
    Args:
        model: SQLAlchemy model class
        **kwargs: Attributes to filter by and use for creation
        
    Returns:
        tuple: (instance, created) where created is a boolean
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    
    instance = model(**kwargs)
    try:
        db.session.add(instance)
        db.session.commit()
        return instance, True
    except SQLAlchemyError:
        db.session.rollback()
        # Try one more time to fetch, in case of a race condition
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            return instance, False
        raise

def soft_delete(instance):
    """
    Mark a record as deleted without removing it from the database.
    Only works with models that have an 'is_deleted' attribute.
    
    Args:
        instance: Model instance to mark as deleted
        
    Returns:
        bool: Success status
    """
    if not hasattr(instance, 'is_deleted'):
        raise AttributeError(f"Model {instance.__class__.__name__} does not support soft delete")
    
    try:
        instance.is_deleted = True
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Soft delete error: {str(e)}")
        return False
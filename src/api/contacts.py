from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, User
from src.services.auth import get_current_user
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    days: int = Query(default=7, ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get a list of contacts with birthdays within the specified number of days.

    Parameters:
    - days (int): Number of days to search for (minimum 1).
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - List[ContactResponse]: List of contacts with upcoming birthdays.
    """
    contact_service = ContactService(db)
    return await contact_service.get_upcoming_birthdays(days, user)


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    name: str = "",
    surname: str = "",
    email: str = "",
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Search for contacts based on filters.

    Parameters:
    - name (str): Contact's first name (optional).
    - surname (str): Contact's last name (optional).
    - email (str): Contact's email (optional).
    - skip (int): Number of records to skip (default 0).
    - limit (int): Maximum number of records to return (default 100).
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - List[ContactResponse]: List of contacts matching the search criteria.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(
        name, surname, email, skip, limit, user
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get contact information by its ID.

    Parameters:
    - contact_id (int): Contact ID.
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - ContactResponse: Contact data.

    Raises:
    - HTTPException (404): If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactModel,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new contact.

    Parameters:
    - body (ContactModel): New contact data.
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - ContactResponse: Data of the created contact.
    """
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update contact data by its ID.

    Parameters:
    - body (ContactModel): New contact data.
    - contact_id (int): Contact ID.
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - ContactResponse: Updated contact data.

    Raises:
    - HTTPException (404): If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Delete a contact by its ID.

    Parameters:
    - contact_id (int): Contact ID.
    - db (AsyncSession): Database session.
    - user (User): Current authenticated user.

    Returns:
    - ContactResponse: Data of the deleted contact.

    Raises:
    - HTTPException (404): If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact

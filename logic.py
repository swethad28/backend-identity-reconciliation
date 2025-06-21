# logic.py

from sqlalchemy.orm import Session
from models import Contact, LinkPrecedenceEnum
from schemas import IdentifyRequest, IdentifyResponse
from typing import List

def process_contact(payload: IdentifyRequest, db: Session) -> IdentifyResponse:
    email = payload.email
    phone = payload.phoneNumber

    if not email and not phone:
        raise ValueError("At least one of email or phoneNumber is required.")

    # Step 1: Find contacts with matching email or phone
    matched_contacts = db.query(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phone)
    ).all()

    if not matched_contacts:
        # No match: create new primary contact
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence=LinkPrecedenceEnum.primary
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return IdentifyResponse(
            primaryContactId=new_contact.id,
            emails=[new_contact.email] if new_contact.email else [],
            phoneNumbers=[new_contact.phoneNumber] if new_contact.phoneNumber else [],
            secondaryContactIds=[]
        )

    # Step 2: Gather all related contact IDs (linked)
    contact_ids = set()
    for contact in matched_contacts:
        contact_ids.add(contact.id)
        if contact.linkedId:
            contact_ids.add(contact.linkedId)

    all_related_contacts = db.query(Contact).filter(
        (Contact.id.in_(contact_ids)) | (Contact.linkedId.in_(contact_ids))
    ).all()

    # Step 3: Determine the primary contact (earliest created)
    primary_contact = min(all_related_contacts, key=lambda c: c.createdAt)

    # Step 4: Check if new info needs to be added
    existing_emails = {c.email for c in all_related_contacts if c.email}
    existing_phones = {c.phoneNumber for c in all_related_contacts if c.phoneNumber}

    is_new_email = email and email not in existing_emails
    is_new_phone = phone and phone not in existing_phones

    if is_new_email or is_new_phone:
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence=LinkPrecedenceEnum.secondary,
            linkedId=primary_contact.id
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        all_related_contacts.append(new_contact)

    # Step 5: Build final response
    emails = list({c.email for c in all_related_contacts if c.email})
    phones = list({c.phoneNumber for c in all_related_contacts if c.phoneNumber})
    secondary_ids = [c.id for c in all_related_contacts if c.linkPrecedence == LinkPrecedenceEnum.secondary]

    return IdentifyResponse(
        primaryContactId=primary_contact.id,
        emails=emails,
        phoneNumbers=phones,
        secondaryContactIds=secondary_ids
    )

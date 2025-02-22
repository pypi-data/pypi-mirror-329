from typing import Dict, Any, Optional
from datetime import datetime,timezone
from fastapi import HTTPException
from google.cloud import firestore
from .exceptions import ResourceNotFoundError, ValidationError

class BaseFirestoreService:
    def __init__(self, db: firestore.Client, collection_name: str, resource_type: str):
        self.db = db
        self.collection_name = collection_name
        self.resource_type = resource_type

    def _validate_update_fields(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Centralized update fields validation"""
        if not isinstance(update_data, dict):
            update_data = update_data.model_dump(exclude_unset=True)
            
        valid_fields = {
            k: v for k, v in update_data.items()
            if v is not None and not (isinstance(v, (list, dict, set)) and len(v) == 0)
        }
        
        if not valid_fields:
            raise ValidationError(
                resource_type=self.resource_type,
                detail="No valid fields to update",
                resource_id=None
            )
            
        return valid_fields

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get a document by ID with standardized error handling"""
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ResourceNotFoundError(
                resource_type=self.resource_type,
                resource_id=doc_id,
                additional_info={"collection": self.collection_name}
            )
            
        return doc.to_dict()

    async def update_document(self, doc_id: str, update_data: Dict[str, Any], user_uid: Optional[str] = None) -> Dict[str, Any]:
        """Standard update method with validation and audit fields"""
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            
            if not doc_ref.get().exists:
                raise ResourceNotFoundError(
                    resource_type=self.resource_type,
                    resource_id=doc_id,
                    additional_info={"collection": self.collection_name}
                )
            
            valid_fields = self._validate_update_fields(update_data)
            
            # Add audit fields
            valid_fields.update({
                'updt_date': datetime.now(timezone.utc).isoformat(),
                'updt_by_user': user_uid if user_uid else None
            })
            
            doc_ref.update(valid_fields)
            return doc_ref.get().to_dict()
            
        except (ResourceNotFoundError, ValidationError):
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update {self.resource_type}: {str(e)}"
            )

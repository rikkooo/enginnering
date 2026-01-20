"""
FreeCAD Document Management Handlers

Handlers for document creation, saving, loading, and management.
"""

from typing import Optional, List, Dict, Any
from .handlers import handler


def _ensure_document(name: str = "Unnamed") -> "FreeCAD.Document":
    """Ensure a document exists, creating one if needed."""
    import FreeCAD
    
    if FreeCAD.ActiveDocument is None:
        return FreeCAD.newDocument(name)
    return FreeCAD.ActiveDocument


@handler("new_document")
def new_document(name: str = "Unnamed") -> dict:
    """
    Create a new FreeCAD document.
    
    Args:
        name: Name for the new document
        
    Returns:
        dict with document info
    """
    import FreeCAD
    
    doc = FreeCAD.newDocument(name)
    
    return {
        "name": doc.Name,
        "label": doc.Label,
        "object_count": len(doc.Objects),
        "success": True
    }


@handler("get_active_document")
def get_active_document() -> dict:
    """
    Get information about the active document.
    
    Returns:
        dict with active document info or None if no document
    """
    import FreeCAD
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return {
            "active": False,
            "name": None,
            "message": "No active document"
        }
        
    return {
        "active": True,
        "name": doc.Name,
        "label": doc.Label,
        "object_count": len(doc.Objects),
        "objects": [obj.Name for obj in doc.Objects]
    }


@handler("list_documents")
def list_documents() -> dict:
    """
    List all open documents.
    
    Returns:
        dict with list of document names
    """
    import FreeCAD
    
    docs = []
    for name in FreeCAD.listDocuments():
        doc = FreeCAD.getDocument(name)
        docs.append({
            "name": doc.Name,
            "label": doc.Label,
            "object_count": len(doc.Objects)
        })
        
    return {
        "documents": docs,
        "count": len(docs),
        "active": FreeCAD.ActiveDocument.Name if FreeCAD.ActiveDocument else None
    }


@handler("close_document")
def close_document(name: str) -> dict:
    """
    Close a document by name.
    
    Args:
        name: Name of the document to close
        
    Returns:
        dict with success status
    """
    import FreeCAD
    
    doc = FreeCAD.getDocument(name)
    if doc is None:
        return {
            "success": False,
            "message": f"Document '{name}' not found"
        }
        
    FreeCAD.closeDocument(name)
    
    return {
        "success": True,
        "closed": name
    }


@handler("save_document")
def save_document(filepath: str, name: Optional[str] = None) -> dict:
    """
    Save a document to a file.
    
    Args:
        filepath: Path to save the document to
        name: Document name (uses active if not specified)
        
    Returns:
        dict with success status
    """
    import FreeCAD
    
    if name:
        doc = FreeCAD.getDocument(name)
    else:
        doc = FreeCAD.ActiveDocument
        
    if doc is None:
        return {
            "success": False,
            "message": "No document to save"
        }
        
    doc.saveAs(filepath)
    
    return {
        "success": True,
        "document": doc.Name,
        "filepath": filepath
    }


@handler("open_document")
def open_document(filepath: str) -> dict:
    """
    Open a document from a file.
    
    Args:
        filepath: Path to the document file
        
    Returns:
        dict with document info
    """
    import FreeCAD
    
    doc = FreeCAD.openDocument(filepath)
    
    return {
        "success": True,
        "name": doc.Name,
        "label": doc.Label,
        "object_count": len(doc.Objects),
        "filepath": filepath
    }


@handler("set_active_document")
def set_active_document(name: str) -> dict:
    """
    Set the active document by name.
    
    Args:
        name: Name of the document to activate
        
    Returns:
        dict with success status
    """
    import FreeCAD
    
    doc = FreeCAD.getDocument(name)
    if doc is None:
        return {
            "success": False,
            "message": f"Document '{name}' not found"
        }
        
    FreeCAD.setActiveDocument(name)
    
    return {
        "success": True,
        "active": name
    }

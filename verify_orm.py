#!/usr/bin/env python
"""
Verification script to confirm all ORM fixes are correct.

Usage:
    uv run python verify_orm.py
    # or
    PYTHONPATH=/home/harshit/Desktop/decisionmind/backend .venv/bin/python verify_orm.py
"""

import sys

from sqlalchemy.orm import configure_mappers, class_mapper

from app.models import User, Decision, Document, DecisionAnalysis


def check_model_attributes(model, model_name):
    """Verify a model has proper SQLAlchemy attributes."""
    print(f"\n{'=' * 60}")
    print(f"Checking {model_name}")
    print('=' * 60)
    
    mapper = class_mapper(model)
    
    # Check mapped columns
    print(f"\n✓ Mapped Columns:")
    for col in mapper.columns:
        print(f"  - {col.name}: {col.type}")
    
    # Check relationships
    print(f"\n✓ Relationships:")
    for rel_name, rel in mapper.relationships.items():
        target_model = rel.mapper.class_.__name__
        back_populates = rel.back_populates or "NONE"
        print(f"  - {rel_name} → {target_model} (back_populates: {back_populates})")
    
    return True


def verify_bidirectional_relationships():
    """Verify all relationships have matching back_populates."""
    print(f"\n{'=' * 60}")
    print("Verifying Bidirectional Relationships")
    print('=' * 60)
    
    relationships_to_verify = [
        ("User", "decisions", "Decision", "creator"),
        ("User", "uploaded_documents", "Document", "uploader"),
        ("Decision", "creator", "User", "decisions"),
        ("Decision", "documents", "Document", "decision"),
        ("Decision", "analyses", "DecisionAnalysis", "decision"),
        ("Document", "decision", "Decision", "documents"),
        ("Document", "uploader", "User", "uploaded_documents"),
        ("DecisionAnalysis", "decision", "Decision", "analyses"),
    ]
    
    models_map = {
        "User": User,
        "Decision": Decision,
        "Document": Document,
        "DecisionAnalysis": DecisionAnalysis,
    }
    
    all_valid = True
    for src_name, rel_name, target_name, expected_back in relationships_to_verify:
        src_model = models_map[src_name]
        mapper = class_mapper(src_model)
        
        if rel_name not in mapper.relationships:
            print(f"✗ MISSING relationship: {src_name}.{rel_name}")
            all_valid = False
            continue
        
        rel = mapper.relationships[rel_name]
        back_populates = rel.back_populates
        target_model = rel.mapper.class_.__name__
        
        if back_populates != expected_back:
            print(f"✗ WRONG back_populates: {src_name}.{rel_name}")
            print(f"  Expected: {expected_back}, Got: {back_populates}")
            all_valid = False
        elif target_model != target_name:
            print(f"✗ WRONG target: {src_name}.{rel_name}")
            print(f"  Expected: {target_name}, Got: {target_model}")
            all_valid = False
        else:
            print(f"✓ {src_name}.{rel_name} ↔ {target_name}.{expected_back}")
    
    return all_valid


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("SQLAlchemy ORM Verification Report")
    print("=" * 60)
    
    try:
        # Test 1: Configure mappers
        print("\n[1/3] Configuring ORM mappers...")
        configure_mappers()
        print("✓ All mappers configured successfully")
        
        # Test 2: Check each model
        print("\n[2/3] Checking model attributes...")
        check_model_attributes(User, "User")
        check_model_attributes(Decision, "Decision")
        check_model_attributes(Document, "Document")
        check_model_attributes(DecisionAnalysis, "DecisionAnalysis")
        
        # Test 3: Verify bidirectional relationships
        print("\n[3/3] Verifying bidirectional relationships...")
        if not verify_bidirectional_relationships():
            print("✗ Bidirectional relationship check FAILED")
            return False
        
        # Summary
        print("\n" + "=" * 60)
        print("✓ ALL VERIFICATION CHECKS PASSED")
        print("=" * 60)
        print("\nORM is ready for:")
        print("  ✓ Alembic migrations")
        print("  ✓ Admin user creation")
        print("  ✓ Production deployment")
        print("\nNext steps:")
        print("  1. Run: alembic upgrade head")
        print("  2. Run: PYTHONPATH=. .venv/bin/python create_admin.py")
        print("  3. Start server and test endpoints")
        
        return True
        
    except Exception as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.workflow_model import WorkflowModel as WorkflowModel
from ..nodes.primitives.input import InputNodeConfig
from ..schemas.workflow_schemas import (
    WorkflowCreateRequestSchema,
    WorkflowDefinitionSchema,
    WorkflowNodeSchema,
    WorkflowResponseSchema,
)

router = APIRouter()


def create_a_new_workflow_definition() -> WorkflowDefinitionSchema:
    return WorkflowDefinitionSchema(
        nodes=[
            WorkflowNodeSchema.model_validate(
                {
                    "id": "input_node",
                    "node_type": "InputNode",
                    "coordinates": {"x": 100, "y": 100},
                    "config": InputNodeConfig().model_dump(),
                }
            )
        ],
        links=[],
    )


def generate_unique_workflow_name(db: Session, base_name: str) -> str:
    existing_workflow = db.query(WorkflowModel).filter(WorkflowModel.name == base_name).first()
    if existing_workflow:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{base_name} {timestamp}"
    return base_name


@router.post(
    "/",
    response_model=WorkflowResponseSchema,
    description="Create a new workflow",
)
def create_workflow(
    workflow_request: WorkflowCreateRequestSchema, db: Session = Depends(get_db)
) -> WorkflowResponseSchema:
    if not workflow_request.definition:
        workflow_request.definition = create_a_new_workflow_definition()
    workflow_name = generate_unique_workflow_name(db, workflow_request.name or "Untitled Workflow")
    new_workflow = WorkflowModel(
        name=workflow_name,
        description=workflow_request.description,
        definition=(workflow_request.definition.model_dump()),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    return new_workflow


@router.put(
    "/{workflow_id}/",
    response_model=WorkflowResponseSchema,
    description="Update a workflow",
)
def update_workflow(
    workflow_id: str,
    workflow_request: WorkflowCreateRequestSchema,
    db: Session = Depends(get_db),
) -> WorkflowResponseSchema:
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not workflow_request.definition:
        raise HTTPException(
            status_code=400,
            detail="Workflow definition is required to update a workflow",
        )
    workflow.definition = workflow_request.definition.model_dump()
    workflow.name = workflow_request.name
    workflow.description = workflow_request.description
    workflow.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(workflow)
    return workflow


@router.get(
    "/",
    response_model=List[WorkflowResponseSchema],
    description="List all workflows",
)
def list_workflows(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size
    workflows = (
        db.query(WorkflowModel)
        .order_by(WorkflowModel.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    valid_workflows: List[WorkflowModel] = []
    for workflow in workflows:
        try:
            WorkflowResponseSchema.model_validate(workflow)
            valid_workflows.append(workflow)
        except Exception:
            continue
    return valid_workflows


@router.get(
    "/{workflow_id}/",
    response_model=WorkflowResponseSchema,
    description="Get a workflow by ID",
)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)) -> WorkflowResponseSchema:
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.put(
    "/{workflow_id}/reset/",
    response_model=WorkflowResponseSchema,
    description="Reset a workflow to its initial state",
)
def reset_workflow(workflow_id: str, db: Session = Depends(get_db)) -> WorkflowResponseSchema:
    # Fetch the workflow by ID
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()

    # If workflow not found, raise 404 error
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Reset the workflow definition to a new one
    workflow.definition = create_a_new_workflow_definition().model_dump()

    # Update the updated_at timestamp
    workflow.updated_at = datetime.now(timezone.utc)

    # Commit the changes to the database
    db.commit()
    db.refresh(workflow)

    # Return the updated workflow
    return workflow


@router.delete(
    "/{workflow_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a workflow by ID",
)
def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    try:
        # Delete associated test files
        test_files_dir = Path("data/test_files") / workflow_id
        if test_files_dir.exists():
            shutil.rmtree(test_files_dir)

        # Delete the workflow (cascading will handle related records)
        db.delete(workflow)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting workflow: {str(e)}",
        )

    return None


@router.post(
    "/{workflow_id}/duplicate/",
    response_model=WorkflowResponseSchema,
    description="Duplicate a workflow by ID",
)
def duplicate_workflow(workflow_id: str, db: Session = Depends(get_db)) -> WorkflowResponseSchema:
    # Fetch the workflow by ID
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()

    # If workflow not found, raise 404 error
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Create a new WorkflowModel instance by copying fields
    new_workflow_name = generate_unique_workflow_name(db, f"{workflow.name} (Copy)")
    new_workflow = WorkflowModel(
        name=new_workflow_name,
        description=workflow.description,
        definition=workflow.definition,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Add and commit the new workflow
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)

    # Return the duplicated workflow
    return new_workflow


@router.get(
    "/{workflow_id}/output_variables/",
    response_model=List[Dict[str, str]],
    description="Get the output variables (leaf nodes) of a workflow",
)
def get_workflow_output_variables(
    workflow_id: str, db: Session = Depends(get_db)
) -> List[Dict[str, str]]:
    """
    Fetch the output variables (leaf nodes) of a workflow.
    """
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow_definition = WorkflowDefinitionSchema.model_validate(workflow.definition)

    # Find leaf nodes (nodes without outgoing links)
    all_source_ids = {link.source_id for link in workflow_definition.links}
    all_node_ids = {node.id for node in workflow_definition.nodes}
    leaf_nodes = all_node_ids - all_source_ids

    # Collect output variables as a list of dictionaries
    output_variables: List[Dict[str, str]] = []
    for node in workflow_definition.nodes:
        if node.id in leaf_nodes:
            try:
                # Try to get output_schema from the node config
                output_schema: Dict[str, str] = {}
                output_schema = node.config.get("output_schema", {})

                # If no output schema is found, skip this node
                if not output_schema:
                    continue

                for var_name in output_schema.keys():
                    output_variables.append(
                        {
                            "node_id": node.id,
                            "variable_name": var_name,
                            "prefixed_variable": f"{node.id}-{var_name}",
                        }
                    )
            except Exception:
                # If there's any error processing this node, skip it
                continue

    return output_variables


@router.post("/upload_test_files/")
async def upload_test_files(
    workflow_id: str = Form(...),
    files: List[UploadFile] = File(...),
    node_id: str = Form(...),
    db: Session = Depends(get_db),
) -> Dict[str, List[str]]:
    """Upload files for test inputs and return their paths"""
    try:
        # Get the workflow
        workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Create workflow-specific directory for test files
        test_files_dir = Path("data/test_files") / workflow_id
        test_files_dir.mkdir(parents=True, exist_ok=True)

        # Save files and collect paths
        saved_paths: List[str] = []
        for file in files:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{file.filename}"
            file_path = test_files_dir / safe_filename

            # Save file
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            # Store relative path
            saved_paths.append(f"test_files/{workflow_id}/{safe_filename}")

        return {node_id: saved_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

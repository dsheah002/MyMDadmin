from app import app, db
from app.models import User, EditHistory
from app.models_glue import GlueType, GlueDescription
from app.models_lead import LeadType, LeadDescription
from app.models_mold import MoldType, MoldDescription
from app.models_wafer import WaferType, WaferDescription


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'EditHistory': EditHistory,
            'GlueType': GlueType, 'GlueDescription': GlueDescription,
            'LeadType': LeadType, 'LeadDescription': LeadDescription,
            'MoldType': MoldType, 'MoldDescription': MoldDescription,
            'WaferType': WaferType, 'WaferDescription': WaferDescription}


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

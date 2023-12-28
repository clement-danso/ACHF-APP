from import_export import resources
from smsapp.models import records

class recordsResource(resources.ModelResource):
    class Meta:
        model = records



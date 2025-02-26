# Generic Table

A Python package that provides features for managing and manipulating tables with:

- **Pagination**
- **Filtering**
- **Sorting**
- **Excel Data Export**

That provides the GenericTable frontend component with everything it needs.

## 📦 Installation

### Install via `pip`

To install the package from PyPI, run the following command:

```bash
pip install generic-table
```

## Usage

### View Table Data with Pagination, Filtering, and Sorting

Use the `view` function to apply pagination, filtering, and sorting to a Django queryset. Here’s an example:

```python
from myapp.models import WorkOrder
from generic_table import view  # Importing the view function from the package

def get_work_orders(request):
    # Get all work orders (simple queryset)
    qs = WorkOrder.objects.all()

    # Define the counted values for the 'status' field
    counted_values = ['IN_PROGRESS', 'APPROVED', 'CANCELLED', 'COMPLETED']

    # Use the `view` function from the `generic_table` package to return the response
    return view(
        qs,
        request,
        field="status",  # The field to count/filter by
        counted_values=counted_values,
        values_list=[
            "id", "status", "number", "description"
        ],  # Fields to return in the response
        data_key="workOrders",  # The key to map the data in the response
    )

```

### 2. Handling Excel Exports

You can also export table data to Excel.
It looks for an `Accept` header with value of `"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"`

```python
from generic_table.generic_table import view
from myapp.models import MyModel

def export_data(request):
    queryset = MyModel.objects.all()
    field = 'status'
    counted_values = ['active', 'inactive']
    return view(queryset, request, field, counted_values, values_list=['status', 'id'])
```

import frappe
import json
from test_narendra.utils.calculator import compute_overall_avg, compute_monthly_tariffs

def before_save(doc, method):
    avg_data = compute_overall_avg(doc.customer_name)
    monthly_data = compute_monthly_tariffs(doc.customer_name)

    doc.overall_avg = avg_data.get("average_kw", 0) + avg_data.get("average_kwh", 0)
    doc.monthly_tariffs = json.dumps(monthly_data)

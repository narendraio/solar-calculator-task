import frappe
from datetime import datetime

def get_tariff_period(ts):
    """
    Determine tariff period based on hour of the day.
    Low: 11PM to 6AM, High: 6AM to 11PM
    """
    # Ensure ts is a datetime object
    if not isinstance(ts, datetime):
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts)
            except ValueError:
                # Default to current time if parsing fails
                ts = datetime.now()
        else:
            ts = datetime.now()
    
    hour = ts.hour
    return "Low" if hour >= 23 or hour < 6 else "High"

def compute_overall_avg(customer=None):
    """
    Compute the overall average KW and KWH values for a customer
    """
    try:
        filters = {}
        if customer:
            filters['customer_name'] = customer

        entries = frappe.get_all("Calculation Entry", filters=filters, fields=["kw", "kwh"])
        if not entries:
            return {"average_kw": 0, "average_kwh": 0}

        # Filter out entries with None values and use default of 0
        valid_entries = []
        for entry in entries:
            valid_entry = {
                "kw": float(entry.kw) if entry.kw is not None else 0,
                "kwh": float(entry.kwh) if entry.kwh is not None else 0
            }
            valid_entries.append(valid_entry)
        
        if not valid_entries:
            return {"average_kw": 0, "average_kwh": 0}
            
        # Calculate averages
        total_kw = sum(entry["kw"] for entry in valid_entries)
        total_kwh = sum(entry["kwh"] for entry in valid_entries)
        count = len(valid_entries)

        return {
            "average_kw": round(total_kw / count, 2) if count > 0 else 0,
            "average_kwh": round(total_kwh / count, 2) if count > 0 else 0
        }
    except Exception as e:
        frappe.log_error(f"Error in compute_overall_avg: {str(e)}")
        return {"average_kw": 0, "average_kwh": 0}

def compute_monthly_tariffs(customer=None):
    """
    Compute monthly tariffs based on kwh usage during high and low periods
    """
    try:
        filters = {}
        if customer:
            filters['customer_name'] = customer

        entries = frappe.get_all("Calculation Entry", filters=filters, fields=["timestamp", "kwh"])
        if not entries:
            return {}

        monthly_data = {}

        for entry in entries:
            # Skip entries with invalid timestamps
            if not entry.timestamp:
                continue
                
            # Ensure timestamp is a datetime object
            if not isinstance(entry.timestamp, datetime):
                try:
                    if isinstance(entry.timestamp, str):
                        # Try to parse ISO format
                        entry.timestamp = datetime.fromisoformat(entry.timestamp)
                    elif isinstance(entry.timestamp, (int, float)):
                        # Try to convert from timestamp
                        entry.timestamp = datetime.fromtimestamp(entry.timestamp)
                    else:
                        # Skip entries with unparseable timestamps
                        continue
                except:
                    # Skip entries with unparseable timestamps
                    continue
            
            # Extract month and determine tariff period
            month = entry.timestamp.strftime("%Y-%m")
            period = get_tariff_period(entry.timestamp)
            
            # Default kwh to 0 if None
            kwh_value = float(entry.kwh) if entry.kwh is not None else 0
            
            # Initialize monthly data structure if needed
            monthly_data.setdefault(month, {"Low": [], "High": []})
            monthly_data[month][period].append(kwh_value)

        result = {}
        for month, values in monthly_data.items():
            # Calculate low tariff average (rate: 0.1)
            low_values = values.get("Low", [])
            low_avg = sum(low_values) / len(low_values) if low_values else 0
            
            # Calculate high tariff average (rate: 0.3)
            high_values = values.get("High", [])
            high_avg = sum(high_values) / len(high_values) if high_values else 0

            # Store tariff calculations
            result[month] = {
                "low_tariff": round(low_avg * 0.1, 2),  # Low period rate is 0.1
                "high_tariff": round(high_avg * 0.3, 2)  # High period rate is 0.3
            }

        return result
    except Exception as e:
        frappe.log_error(f"Error in compute_monthly_tariffs: {str(e)}")
        return {}
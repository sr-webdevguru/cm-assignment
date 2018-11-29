from apps.controlled_substance.models import AuditLog
from apps.controlled_substance.models import IN, OUT, USED
from helper_functions import sort_drug_administered_by


def add_log(log_entry, resort, user):
    audit_log = AuditLog(log_entry=log_entry, resort=resort, added_by_user=user)
    audit_log.save()

    return audit_log


def stock_status_count(data):
    in_count = 0
    out_count = 0
    used_count = 0
    disposed_count = 0
    for each_data in data:
        if each_data.current_status == IN:
            in_count += 1
        elif each_data.current_status == OUT:
            out_count += 1
        elif each_data.current_status == USED:
            used_count += 1

    return {
        "in": in_count,
        "out": out_count,
        "used": used_count
    }


def add_stock_entry_to_config(resort, stock, user):
    controlled_substance_key = None
    stock_id = str(stock.controlled_substance_stock_id)
    controlled_substance_name = stock.controlled_substance.controlled_substance_name
    user_name = user.name

    # Check for existence of substance entry in the config
    config = resort.incident_template

    try:
        drug_field = config['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e'][
            'RepeatingQuestions']
        drug_administered_field = drug_field['drug_administered']
    except:
        return False, "drug_administered field not found"

    for value in drug_administered_field['Values']:
        if 'controlled' in value:
            for key, val in value.iteritems():
                if val.lower() == controlled_substance_name.lower():
                    controlled_substance_key = key

    if controlled_substance_key is not None:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_key
    else:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_name

    if drug_administered_by_key in drug_field:
        drug_administered_by = drug_field[drug_administered_by_key]
        drug_administered_by_values = drug_administered_by['Values']
        drug_administered_by_values.append({stock_id: str(stock.controlled_substance_stock_pk) + " " + user_name})
        drug_administered_by['Values'] = sort_drug_administered_by(drug_administered_by_values)
    else:
        drug_field[drug_administered_by_key] = {
            "Label": "drug_administered_by",
            "ParentKey": "drug_administered_by",
            "Placeholder": "",
            "Type": "select",
            "Required": "true",
            "Order": 0,
            "Values": [
                {stock_id: str(stock.controlled_substance_stock_pk) + " " + user_name},
            ],
            "ShowIf": {"drug_administered": controlled_substance_key if controlled_substance_key is not None else controlled_substance_name }
        }

    resort.incident_template = config
    resort.save()

    return True, ""


def remove_stock_entry_from_config(resort, stock):
    controlled_substance_name = stock.controlled_substance.controlled_substance_name
    controlled_substance_key = None
    stock_id = str(stock.controlled_substance_stock_id)

    # Check for existence of substance entry in the config
    config = resort.incident_template

    try:
        drug_field = config['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e'][
            'RepeatingQuestions']
        drug_administered_field = drug_field['drug_administered']
    except:
        return False, "drug_administered field not found"

    for value in drug_administered_field['Values']:
        if 'controlled' in value:
            for key, val in value.iteritems():
                if val.lower() == controlled_substance_name.lower():
                    controlled_substance_key = key

    if controlled_substance_key is not None:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_key
    else:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_name

    if drug_administered_by_key in drug_field:
        drug_administered_by = drug_field[drug_administered_by_key]
        drug_administered_by['Values'] = [d for d in drug_administered_by['Values'] if d.keys()[0] != stock_id]

        if not drug_administered_by['Values']:
            del drug_field[drug_administered_by_key]

    resort.incident_template = config
    resort.save()

    return True, ""


def manipulate_string_drug_administered_by(val, stock_id):

    for each_val in val:
        if each_val.keys()[0] == stock_id:
            each_val[each_val.keys()[0]] = "USED " + each_val[each_val.keys()[0]]

    return val


def mark_stock_entry_used(resort, stock):
    controlled_substance_name = stock.controlled_substance.controlled_substance_name
    controlled_substance_key = None
    stock_id = str(stock.controlled_substance_stock_id)

    # Check for existence of substance entry in the config
    config = resort.incident_template

    try:
        drug_field = config['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e'][
            'RepeatingQuestions']
        drug_administered_field = drug_field['drug_administered']
    except:
        return False, "drug_administered field not found"

    for value in drug_administered_field['Values']:
        if 'controlled' in value:
            for key, val in value.iteritems():
                if val.lower() == controlled_substance_name.lower():
                    controlled_substance_key = key

    if controlled_substance_key is not None:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_key
    else:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_name

    if drug_administered_by_key in drug_field:
        drug_administered_by = drug_field[drug_administered_by_key]
        drug_administered_by['Values'] = manipulate_string_drug_administered_by(drug_administered_by['Values'], stock_id)
        drug_administered_by['Values'] = sort_drug_administered_by(drug_administered_by['Values'])

    resort.incident_template = config
    resort.save()

    return True, ""


def unmark_used_stock_entry(resort, stock):
    controlled_substance_name = stock.controlled_substance.controlled_substance_name
    controlled_substance_key = None
    stock_id = str(stock.controlled_substance_stock_id)

    config = resort.incident_template

    try:
        drug_field = config['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e'][
            'RepeatingQuestions']
        drug_administered_field = drug_field['drug_administered']
    except:
        return False, "drug_administered field not found"

    for value in drug_administered_field['Values']:
        if 'controlled' in value:
            for key, val in value.iteritems():
                if val.lower() == controlled_substance_name.lower():
                    controlled_substance_key = key

    if controlled_substance_key is not None:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_key
    else:
        drug_administered_by_key = "drug_administered_by_" + controlled_substance_name

    if drug_administered_by_key in drug_field:
        drug_administered_by = drug_field[drug_administered_by_key]

        for i, each_val in enumerate(drug_administered_by['Values']):
            if each_val.keys()[0] == stock_id:
                drug_administered_by['Values'][i][drug_administered_by['Values'][i].keys()[0]] = drug_administered_by['Values'][i][drug_administered_by['Values'][i].keys()[0]][5:]
                resort.incident_template = config
                resort.save()

    return True, ""
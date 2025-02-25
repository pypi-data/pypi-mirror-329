import json

# ----------------------------------------------------------------
# Sample JSON data
# schemaAJSON = '''
# {
#     "user": {
#         "name": "string",
#         "age": "int",
#         "contact": {
#             "email": "string",
#             "phone": "string"
#         }
#     },
#     "transactions": [
#         {
#             "currency": "string",
#             "amount": "float"
#         },
#         {
#             "currency": "string",
#             "amount": "float"
#         }
#     ]
# }
# '''
#
# mappingJSON = '''
# {
#     "user": "person",
#     "user.name": "person.full_name",
#     "user.age": "person.years_old",
#     "user.contact": "person.details",
#     "user.contact.email": "person.details.mail",
#     "user.contact.phone": "person.details.telephone",
#
#     "transactions": "payments",
#     "transactions[].currency": "payments[].currency_type",
#     "transactions[].amount": "payments[].value"
# }
# '''
# ----------------------------------------------------------------


def _reorder_mapping_by_key(mapping):
    """
    Return a NEW dictionary whose items are sorted by the KEY in alphabetical order.
    """
    # 1) Convert to a list of (key, value) pairs
    items = list(mapping.items())
    # 2) Sort by the key (the src_line) ascending
    items.sort(key=lambda x: x[0])
    # 3) Build a new dictionary in that order
    new_map = {}
    for k, v in items:
        new_map[k] = v
    return new_map

# ----------------------------------------------------------------
# 1) Recursively GET from schemaA with array expansions
# ----------------------------------------------------------------
def _get_multi(obj, path):
    """Extract data from obj along 'dot.path' with possible '[]' array expansions."""
    if not path:
        return obj
    dot_idx = path.find(".")
    if dot_idx == -1:
        seg, remainder = path, ""
    else:
        seg, remainder = path[:dot_idx], path[dot_idx+1:]

    if "[]" in seg:
        key = seg.replace("[]", "")
        if not isinstance(obj, dict):
            return None
        arr = obj.get(key)
        if not isinstance(arr, list):
            return None
        results = []
        for item in arr:
            val = _get_multi(item, remainder)
            if val is None:
                continue
            if isinstance(val, list):
                results.extend(val)
            else:
                results.append(val)
        return results if results else None
    else:
        if not isinstance(obj, dict):
            return None
        nxt = obj.get(seg)
        if nxt is None:
            return None
        return _get_multi(nxt, remainder)

# ----------------------------------------------------------------
# 2) Recursively SET in the result (no special overwrite logic, merges)
# ----------------------------------------------------------------
def _set_multi(obj, path, val):
    """Set 'val' into 'obj' at 'dot.path' with possible '[]' expansions, merging dicts."""
    if not path:
        return
    dot_idx = path.find(".")
    if dot_idx == -1:
        seg, remainder = path, ""
    else:
        seg, remainder = path[:dot_idx], path[dot_idx+1:]
    if "[]" in seg:
        key = seg.replace("[]", "")
        if key not in obj or not isinstance(obj[key], list):
            if isinstance(val, list):
                obj[key] = [{} for _ in range(len(val))]
            else:
                obj[key] = [{}]
        if isinstance(val, list):
            for i, subval in enumerate(val):
                if i >= len(obj[key]):
                    obj[key].append({})
                _merge_dict(obj[key][i], subval)
                _set_multi(obj[key][i], remainder, subval)
        else:
            if not obj[key]:
                obj[key].append({})
            _merge_dict(obj[key][0], val)
            _set_multi(obj[key][0], remainder, val)
    else:
        if seg not in obj or not isinstance(obj[seg], dict):
            obj[seg] = {}
        if remainder == "":
            _merge_dict(obj[seg], val) if isinstance(val, dict) else obj.__setitem__(seg, val)
        else:
            if isinstance(val, dict):
                _merge_dict(obj[seg], val)
            _set_multi(obj[seg], remainder, val)

# ----------------------------------------------------------------
# Helper function to merge 'source' dict into 'dest' dict
# (Just merges keys, leftover fields can appear => we prune later)
# ----------------------------------------------------------------
def _merge_dict(dest, source):
    if not isinstance(source, dict):
        return
    for k, v in source.items():
        dest[k] = v

# ----------------------------------------------------------------
# 3) Build the result applying ALL mapping lines (incl. parents)
# ----------------------------------------------------------------
def _build_full(schemaA, mapping):
    """
    - We do NOT skip parent lines.
    - We apply every line (parent & child).
    - This might create leftover fields. We'll remove them in prune step.
    """
    res = {}
    for src_line, dst_line in mapping.items():
        val = _get_multi(schemaA, src_line)
        if val is not None:
            _set_multi(res, dst_line, val)
    return res

# ----------------------------------------------------------------
# 4) Prune leftover fields that aren't in mapped destinations
# ----------------------------------------------------------------
def _prune_unmapped(obj, mapped_dest_lines, prefix=""):
    """
    Recursively remove leftover keys from 'obj' that do not match or lead to
    a line in 'mapped_dest_lines'. We do a stricter match: line_no_array must
    either be exactly 'short_path' or start with 'short_path.' to keep it.
    """
    if not isinstance(obj, dict):
        return

    keys_to_remove = []
    for k in obj:
        new_path = f"{prefix}.{k}" if prefix else k
        # remove array markers for comparison
        short_path = new_path.replace("[]", "")

        matched = False
        for line in mapped_dest_lines:
            clean_line = line.replace("[]", "")
            # Require either exact match or a '.' boundary
            # e.g. "payments.currency_type" won't match "payments.currency"
            # because we'd need "payments.currency" == "payments.currency_type"
            # or "payments.currency." prefix
            if clean_line == short_path or clean_line.startswith(short_path + "."):
                matched = True
                break

        if not matched:
            # Not a valid path => remove
            keys_to_remove.append(k)
        else:
            # Recurse deeper if it's a dict or list
            val = obj[k]
            if isinstance(val, dict):
                _prune_unmapped(val, mapped_dest_lines, new_path)
            elif isinstance(val, list):
                for i, subitem in enumerate(val):
                    if isinstance(subitem, dict):
                        _prune_unmapped(subitem, mapped_dest_lines, new_path)

    for rk in keys_to_remove:
        del obj[rk]

# ----------------------------------------------------------------
# 5) transform => Build everything + prune leftover
# ----------------------------------------------------------------
def transform(schemaA, mapping):
    schemaA = json.loads(schemaA)
    mapping = json.loads(mapping)
    # A) Build result applying EVERY line (parents & children)
    mapping= _reorder_mapping_by_key(mapping)
    result = _build_full(schemaA, mapping)

    # B) Gather all mapping destination lines => used for prune
    mapped_dest_lines = set(mapping.values())

    # C) Prune leftover fields
    _prune_unmapped(result, mapped_dest_lines)
    return result


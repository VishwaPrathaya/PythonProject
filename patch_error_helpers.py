from pathlib import Path

p = Path('allocation_engine.py')
text = p.read_text(encoding='utf-8')
needle = 'from counters import load_counters, update_counter_file, get_available_counters, create_counter\n\n\n# ---------------- LOAD EXISTING ALLOCATIONS ----------------\n'
idx = text.find(needle)
if idx == -1:
    raise RuntimeError('needle not found')
insert = "from datetime import datetime\n\nallocation_error_log = []\nlast_allocation_error = None\n\n\ndef record_allocation_error(fno, reason):\n    global allocation_error_log, last_allocation_error\n    timestamp = datetime.now().isoformat(timespec='seconds')\n    entry = {'flight': fno, 'reason': reason, 'time': timestamp}\n    allocation_error_log.append(entry)\n    last_allocation_error = entry\n    if len(allocation_error_log) > 30:\n        allocation_error_log.pop(0)\n    try:\n        with open('allocation_error_log.csv', 'a', encoding='utf-8') as f:\n            f.write(f"{timestamp},{fno},{reason}\n")\n    except Exception:\n        pass\n\n\ndef get_recent_allocation_errors(count=10):\n    return allocation_error_log[-count:]\n\n\ndef get_last_allocation_error():\n    return last_allocation_error\n\n\ndef clear_last_allocation_error():\n    global last_allocation_error\n    last_allocation_error = None\n\n"
text = text[:idx+len('from counters import load_counters, update_counter_file, get_available_counters, create_counter\n')] + '\n' + insert + text[idx+len('from counters import load_counters, update_counter_file, get_available_counters, create_counter\n'):]
p.write_text(text, encoding='utf-8')
print('inserted')
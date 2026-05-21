from pathlib import Path

p = Path('allocation_engine.py')
text = p.read_text(encoding='utf-8')
needle = 'from counters import load_counters, update_counter_file, get_available_counters, create_counter\n\n\n# ---------------- LOAD EXISTING ALLOCATIONS ----------------\n'
idx = text.find(needle)
if idx == -1:
    raise RuntimeError('needle not found')
insert = '''from datetime import datetime

allocation_error_log = []
last_allocation_error = None


def record_allocation_error(fno, reason):
    global allocation_error_log, last_allocation_error
    timestamp = datetime.now().isoformat(timespec='seconds')
    entry = {'flight': fno, 'reason': reason, 'time': timestamp}
    allocation_error_log.append(entry)
    last_allocation_error = entry
    if len(allocation_error_log) > 30:
        allocation_error_log.pop(0)
    try:
        with open('allocation_error_log.csv', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp},{fno},{reason}\n")
    except Exception:
        pass


def get_recent_allocation_errors(count=10):
    return allocation_error_log[-count:]


def get_last_allocation_error():
    return last_allocation_error


def clear_last_allocation_error():
    global last_allocation_error
    last_allocation_error = None
'''
text = text[:idx+len('from counters import load_counters, update_counter_file, get_available_counters, create_counter\n')] + '\n' + insert + text[idx+len('from counters import load_counters, update_counter_file, get_available_counters, create_counter\n'):]
p.write_text(text, encoding='utf-8')
print('inserted')

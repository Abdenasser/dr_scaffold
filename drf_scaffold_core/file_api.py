def create_file(path):
  with open(path, 'x') as file:
    file.close()

def wipe_file_content(path):
  with open(path, 'r+') as file:
    file.truncate(0)
    file.close()

def get_file_content(path):
  with open(path, 'r+') as file:
    body = ''.join(line for line in file.readlines())
    file.close()
    return body

def set_file_content(path, body):
  wipe_file_content(path)
  with open(path, 'r+') as file:
    file.write(body)
    file.close()

def prepend_file_content(path, head):
  body = get_file_content(path)
  wipe_file_content(path)
  set_file_content(path, head + "\n" + body)

def append_file_content(path, tail):
  body = get_file_content(path)
  wipe_file_content(path)
  set_file_content(path, body + tail)

def wrap_file_content(path, head, tail):
  prepend_file_content(path, head)
  append_file_content(path, "\n" + tail)

def replace_file_chunk(path, chunk, new):
  body = get_file_content(path)
  body = body.replace(chunk, new)
  wipe_file_content(path)
  set_file_content(path, body)

def is_present_in_file(path, str):
  body = get_file_content(path)
  if str in body:
    return True
  return False
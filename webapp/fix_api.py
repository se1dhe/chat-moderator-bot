import re

with open('src/lib/api.ts', 'r') as f:
    text = f.read()

old_fetch = """    try { 
      const data = await resp.json();
      detail = data.error || detail;
    } catch { /* empty */ }
    const err = new Error(detail) as any;
    err.status = resp.status;
    throw err;"""

new_fetch = """    let responseData = null;
    try { 
      responseData = await resp.json();
      detail = responseData.error || responseData.reason || detail;
    } catch { /* empty */ }
    const err = new Error(detail) as any;
    err.status = resp.status;
    err.response = { data: responseData };
    throw err;"""

text = text.replace(old_fetch, new_fetch)

with open('src/lib/api.ts', 'w') as f:
    f.write(text)


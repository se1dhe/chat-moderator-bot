import re

with open('src/pages/Triggers.tsx', 'r') as f:
    text = f.read()

text = text.replace("import { useState, useEffect } from 'react';", "import { useState, useEffect } from 'react';\nimport { showAlert } from '../lib/telegram';")

old_catch1 = """    } catch (e: any) {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.showAlert(e.message);
      } else {
        alert(e.message);
      }
    }"""

new_catch1 = """    } catch (e: any) {
      showAlert(e.message);
    }"""

text = text.replace(old_catch1, new_catch1)

with open('src/pages/Triggers.tsx', 'w') as f:
    f.write(text)


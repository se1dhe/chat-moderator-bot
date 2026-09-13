filename = "webapp/src/pages/Triggers.jsx"
with open(filename, "r") as f:
    text = f.read()

text = text.replace("import { Card, Input, Button, Toggle } from '../components/ui';", "import { Toggle } from '../components/ui';")

text = text.replace("<Card className=\\"p-4 space-y-4\\">", "<div className=\\"card card-pad space-y-4\\">")
text = text.replace("</Card>", "</div>")
text = text.replace('<Card key={t.id} className="p-3 flex justify-between items-start gap-4">', '<div key={t.id} className="card card-pad flex justify-between items-start gap-4">')

# Input replacements
text = text.replace("""<Input 
          label="Phrase or Command" 
          value={word} 
          onChange={(e) => setWord(e.target.value)} 
          placeholder="e.g. /rules or price"
        />""", """<div className="space-y-1">
          <div className="text-sm font-medium">Phrase or Command</div>
          <input className="input w-full" value={word} onChange={(e) => setWord(e.target.value)} placeholder="e.g. /rules or price" />
        </div>""")

text = text.replace("""<Input 
          label="Reply Text" 
          value={reply} 
          onChange={(e) => setReply(e.target.value)} 
          placeholder="The bot will send this..."
          multiline
        />""", """<div className="space-y-1">
          <div className="text-sm font-medium">Reply Text</div>
          <textarea className="input w-full" rows="3" value={reply} onChange={(e) => setReply(e.target.value)} placeholder="The bot will send this..."></textarea>
        </div>""")

# Button replacements
text = text.replace('<Button onClick={handleCreate} disabled={!word || !reply} className="w-full">', '<button className="btn btn-primary w-full" onClick={handleCreate} disabled={!word || !reply}>')
text = text.replace('</Button>', '</button>')
text = text.replace('<Button variant="danger" size="sm" onClick={() => handleDelete(t.id)}>Delete</Button>', '<button className="btn btn-danger" style={{fontSize: "12px", padding: "4px 8px"}} onClick={() => handleDelete(t.id)}>Delete</button>')

with open(filename, "w") as f:
    f.write(text)

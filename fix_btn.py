with open("webapp/src/pages/Triggers.jsx", "r") as f: t = f.read()
t = t.replace("Add Trigger\\n        </button>", "{t(\\"triggers.btn.add\\")}\\n        </button>")
with open("webapp/src/pages/Triggers.jsx", "w") as f: f.write(t)

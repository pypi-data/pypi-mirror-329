# web360


`/docs' contains auto-generated files from [360noscope.gitbook.io](https://360noscope.gitbook.io/web360)
Files must be generated in Gitbook, and are synced to these here.

[360noscope.gitbook](https://app.gitbook.com/o/92bqHwQOS4AmsvwJSGH3/s/pfkqTTnftgbXDg4FUKCF/) is synced to doctorslimms github.
dev@360noscope.co has web360.gitbook.io



`/apps` contains frontend applications

```
apps/                     
│── console/                     # console.web360.dev
│   │── js/tsx
|   ...
│── landing-page/                # web360.dev
│   │── index.html               # Html file to edit
```

Run frontend from subdirectories
```bash
cd apps/console
npm run dev 
```



Tools, interfaces, and Api Types can be found in [/web360/tools](/web360/tools)

The Api which is exposed via [api.web360.dev](api.web360.dev) is run by [/web360/main.py](/web360/main.py)

```
web360/
│── main.py                  # start Api and settings
│── web360.py                # web360 class definition
│── logger.py                
│── deps/                    # Api middleware / auth / logging
│   │── __init__.py        
│── tools/                   # llm tool definitions and models
│   │── __init__.py        
│   ├── search.py            # contains SearchTool that is a Pydantic object with description, summary, examples, and endpoint
│   ├── ...
```

Database schemas
```
/models                          # contains sql and json models for cross app compatgibility
apilogs.sql                      # supabase SQL table definition
apilogs.json                     # converted to ts interface for console, and pydantic for Api
...
```


`/web360` Python package 
```bash
pip install web360
```

Api server
```bash
import web360

app = web360.create_app('...')
uvivcorn...
```

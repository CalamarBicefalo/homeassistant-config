# Context
This repo contains Home Assistant (HA) configuration. It includes:
- A bunch of YAML as per the official HA configuration docs
- Some YAML that is generated code via ./generate.py typically (but not always) contains generated in the filename
- Appdaemon python apps. These are all my automations, and are tested in ./appdaemon/tests
- NEVER modify generated files, instead use generate.py
- A dashboard using minimalist UI in ./ui_lovelace_minimalist/dashboard

# Rules for agents to follow
- Do not make assumptions, always check with me. Ask clarifying questions if 
there's ambiguity in the task at hand.
- Comments are good, but do not add superfluous or overly verbose comments for the sake of it
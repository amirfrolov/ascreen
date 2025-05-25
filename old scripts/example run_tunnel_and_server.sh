#!/bin/bash
bash screen_restart.sh tunnel "cloudflared tunnel run my-tunnel"
bash screen_restart.sh server "cd finexo-html; python -m http.server 8083"

#print the screens
screen -ls
echo "Reattach to a Screen Session:
screen -r tunnel
screen -r server
To exit a screen session Without Closing It: Ctrl+A+D
bash close_tunnel_and_server.sh"

